import json
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Conversation, Message, Profile
from .serializers import ConversationSerializer, MessageSerializer, ProfileSerializer
import datetime
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import random
import requests
from utils.try_except_block import DefaultAvatarTryExceptBlock, RealAvatarTryExceptBlock

@api_view(['GET'])
def get_messages_from_conversation(request, pk):
    # gets all messages belonging to certain conversation
    conversation = Conversation.objects.get(id=pk)
    messages = conversation.messages.all()
    serialized = MessageSerializer(messages, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def get_conversation_from_message(request, pk):
    # gets conversation to which certain message belongs
    message = Message.objects.get(id=pk)
    conversation = message.conversation
    serialized = ConversationSerializer(conversation, many=False)
    return Response(serialized.data)


@api_view(['GET'])
def get_conversations_from_user(request, pk):
    # get all conversations to which user belongs
    user = User.objects.get(id=pk)
    conversations = user.conversation.all()
    message_list = []
    serialized_convos = ConversationSerializer(conversations, many=True)
    # loop through serialized conversations
    for convo in serialized_convos.data:
        # get id of each conversation

        convo_id = convo['id']
        # get messages that belong to the above convo
        messages = Message.objects.filter(conversation_id=int(convo_id))
        serialized_messages = MessageSerializer(messages, many=True)
        # loop  through messages belonging to each conversation
        for message in serialized_messages.data:
            # convert django garbage date format to normal
            created_on = message['created_on']
            created_on = datetime.datetime.strptime(created_on, '%Y-%m-%dT%H:%M:%S.%fZ')
            created_on = created_on.strftime("%d.%m.%Y %H:%M:%S")
            # created_on = created_on.strftime("%d.%m.%Y %H:%M")
            message_list.append({
                'convo_id': convo_id,
                'message': message['message'],
                'created_on': created_on,
                'created_by': message['created_by']
            })
            convo['messages'] = message_list
        # clear the list so that each conversation is attached only its own messages
        message_list = []
    # Sort data based on messages belonging to each convo; convo with newest message is first in list etc
    sorted_data = sorted(
        serialized_convos.data,
        key=lambda x: max(
            datetime.datetime.strptime(msg["created_on"], "%d.%m.%Y %H:%M:%S")
            for msg in x.get("messages")
        )
        # if a convo doesnt have messages yet
        if "messages" in x
        else datetime.datetime(1970, 1, 1),
        reverse=True, )
    return Response(sorted_data)


@api_view(['GET'])
def get_partner_and_last_message_from_user(request, pk):
    # Get conversation partner and last message from conversation
    # active user sending request
    requesting_user = User.objects.get(id=pk)
    # conversations belonging to active user
    conversations = requesting_user.conversation.all()
    # print(f'length of convo queryset: {len(conversations)}')
    conversation_list = []
    # loop through their conversation objects
    for conversation in conversations:
        # loop through members belonging to each conversation the active user is apart of
        for member in conversation.members.all():
            # if the member of the conversation isnt the active user its the convo partner
            if member != requesting_user:
                convo_partner_user = User.objects.get(id=member.id)
                profile = Profile.objects.get(user_id=member.id)

                encoded_default_avatar = DefaultAvatarTryExceptBlock(convo_partner_user, profile)
                encoded_real_avatar = RealAvatarTryExceptBlock(convo_partner_user, profile)

                # for case when new chat was created but there are no messages exchanged yet
                if conversation.messages.last() is not None:
                    last_message = conversation.messages.last().message
                    message_created_on = conversation.messages.last().created_on
                else:
                    # if there is no actual message to use, set the created_on time to 2050 so that the convo is put
                    # at the bottom of the list when it's sorted
                    last_message = ''
                    message_created_on = datetime.datetime.strptime('03.07.2010 18:04:54', '%d.%m.%Y %H:%M:%S')
                conversation_list.append(
                    {
                        'conv_id': conversation.id,
                        'conv_partner': member.username,
                        'conv_partner_real_name': profile.real_name,
                        'last_message': last_message,
                        'created_on': message_created_on if message_created_on == '' else
                        message_created_on.strftime("%d.%m.%Y %H:%M:%S"),
                        'avatar': encoded_default_avatar,
                        'real_avatar': encoded_real_avatar,
                        'is_online': profile.is_online

                    }

                )
    sorted_data = sorted(conversation_list,
                         key=lambda x: datetime.datetime.strptime(x['created_on'], '%d.%m.%Y %H:%M:%S'),
                         reverse=True)
    return Response(sorted_data)


@api_view(['GET'])
def get_messages_with_user(request, pk, name):
    active_user = User.objects.get(id=pk)
    # all convos belonging to that user
    conversations = active_user.conversation.all()
    conv_partner_user = User.objects.get(username=name)
    conv_partner_profile = Profile.objects.get(user_id=conv_partner_user.id)
    # if the user hasnt set their avatar or real avatar, use a pre-made one
    encoded_default_avatar = DefaultAvatarTryExceptBlock(conv_partner_user, conv_partner_profile)
    # if not Profile.objects.get(user_id=conv_partner_user.id).avatar:
    #     with open('avatars/default_avatar.png', "rb") as image_file:
    #         encoded_avatar = base64.b64encode(image_file.read())
    # else:
    #     with open(str(Profile.objects.get(user_id=conv_partner_user.id).avatar), "rb") as image_file:
    #         encoded_avatar = base64.b64encode(image_file.read())
    sorted_data = []
    # loop through all their conversation objects
    for convo in conversations:
        # loop through members of each conversation
        for member in convo.members.all():
            # match conversation partner to the name parameter passed
            if member.username == name:
                member_profile = Profile.objects.get(user_id=member.id)
                user = User.objects.get(id=member.id)
                encoded_real_avatar = RealAvatarTryExceptBlock(user, member_profile)
                # if not profile.real_avatar:
                #     with open('avatars/default_avatar.png', "rb") as image_file:
                #         encoded_real_avatar = base64.b64encode(image_file.read())
                # else:
                #     with open(str(profile.real_avatar), "rb") as image_file_2:
                #         encoded_real_avatar = base64.b64encode(image_file_2.read())
                sorted_data.append(
                    {
                        'convo_id': convo.id,
                        'conv_partner': name,
                        'conv_partner_real_name': member_profile.real_name,
                        'avatar': encoded_default_avatar,
                        'real_avatar': encoded_real_avatar,
                        'messages': [],
                        'last_message': convo.messages.last().message if convo.messages.last() is not None else ''
                    }
                )
                # serialize messages belonging to matching convo
                serialized_messages = MessageSerializer(convo.messages.all(), many=True).data
                # loop through messages and append them to list
                for message in serialized_messages:
                    sorted_data[0]['messages'].append({
                        # 'convo_id': convo.id,
                        'message': message['message'],
                        'created_by': message['created_by']
                    })
                return Response(sorted_data)


@api_view(['POST'])
def create_new_message(request):
    # runs every time a new message is sent in chat and creates a new entry in DB
    data = request.data
    convo_id = data['convo_id']
    userID = data['created_by']
    user = User.objects.get(id=userID)
    conversation = Conversation.objects.get(id=convo_id)
    # message_content = request.data['message_content']

    message = Message.objects.create(message=data['message'],
                                     conversation=conversation,
                                     created_by=user,
                                     # senderID=data['senderID'],
                                     # # ownedByCurrentUser=data['ownedByCurrentUser']
                                     )
    # message.save()
    return Response("Message succesfuly saved")


@api_view(['GET'])
def get_user_profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    user = User.objects.get(id=pk)
    encoded_default_avatar = DefaultAvatarTryExceptBlock(user, profile)
    encoded_real_avatar = RealAvatarTryExceptBlock(user, profile)
    return Response([{
        'age': profile.age,
        'gender': profile.gender,
        'location': profile.location,
        'description': profile.description,
        'interests': profile.interests,
        'reason': profile.reason,
        'username': user.username,
        'real_name': profile.real_name,
        'avatar': encoded_default_avatar,
        'real_avatar': encoded_real_avatar,

    }
    ]
    )


@api_view(['POST'])
def reveal_profile(request):
    data = request.data
    user = request.user
    # get conversation in question
    convo = Conversation.objects.get(id=data['conversation'])
    # if neither conversation member has revealed, do it for the first member
    if convo.first_member_reveal == False and convo.second_member_reveal == False:
        convo.first_member_reveal = True
        convo.first_member_id = user.id
        convo.save()
    # if first member is revealed, reveal for the second
    elif convo.first_member_reveal == True and convo.second_member_reveal == False:
        convo.second_member_reveal = True
        convo.second_member_id = user.id
        convo.save()
    elif convo.first_member_reveal == False and convo.second_member_reveal == True:
        convo.first_member_reveal = True
        convo.first_member_id = user.id
        convo.save()
    else:
        return Response('Both profiles already revealed')
    return Response({
        'convo': convo.id,
        'user_id': user.id,
        'clicked': 'true'
    })


@api_view(['POST'])
def hide_profile(request):
    data = request.data
    user = request.user
    # get conversation in question
    convo = Conversation.objects.get(id=data['conversation'])
    # if neither conversation member has revealed, do it for the first member
    if convo.first_member_reveal == True and int(convo.first_member_id) == user.id:
        # print('first scenario match')
        convo.first_member_reveal = False
        convo.save()
    elif convo.second_member_reveal == True and int(convo.second_member_id) == user.id:
        # print('second scenario match')
        convo.second_member_reveal = False
        convo.save()
    else:
        return Response('Neither members profile is revealed')
    return Response({
        'convo': convo.id,
        'user_id': user.id,
        'clicked': 'false'
    })


# after both people click the reveal button, alert will pop up notifying and asking
# if user wants to see the partners profile info > on button click there trigger fetch
# to this endpoint
@api_view(['GET'])
def get_revealed_profiles_from_convo(request, pk):
    convo = Conversation.objects.get(id=pk)
    # check if both users have agreed to reveal
    if convo.first_member_reveal == True and convo.second_member_reveal == True:
        # loop through members of the convo
        for member in convo.members.all():
            # get the conversation partner to return their data
            if request.user != member:
                # print(f'This is the member {member}')
                profile = Profile.objects.get(user_id=member.id)
                member_user = User.objects.get(id=member.id)
                # if not profile.avatar:
                encoded_real_avatar = RealAvatarTryExceptBlock(member_user, profile)
                # if not profile.real_avatar:
                #     with open('avatars/default_avatar.png', "rb") as image_file:
                #         encoded_real_avatar = base64.b64encode(image_file.read())
                # else:
                #     with open(str(profile.real_avatar), "rb") as image_file_2:
                #         encoded_real_avatar = base64.b64encode(image_file_2.read())
                return Response([{
                    'username': member.username,
                    'age': profile.age,
                    'gender': profile.gender,
                    'location': profile.location,
                    'description': profile.description,
                    'interests': profile.interests,
                    'reason': profile.reason,
                    'real_name': profile.real_name,
                    'real_avatar': encoded_real_avatar,
                    # 'id': member.id

                }
                ]
                )
    else:
        return Response('1 or more members havent revealed their profile')


@api_view(['GET'])
def check_reveal_status(request, pk):
    # takes convo id and checks if the user.id of the user making the request matches one of the member_ids
    # the match will only occur if the user has revealed their profile within the convo in question
    convo = Conversation.objects.get(id=pk)
    user = request.user

    # Both members have revealed
    if (convo.second_member_id is not None
            and convo.first_member_id is not None
            and convo.first_member_reveal == True
            and convo.second_member_reveal == True):
        # print('Case 1')
        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': True,
            'partner_revealed': True
        })
    # requesting user is first member, first member has revealed and partner hasnt
    elif convo.first_member_id is not None \
            and user.id == int(convo.first_member_id) \
            and convo.first_member_reveal == True \
            and convo.second_member_reveal == False:
        # print('Case 2')

        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': True,
            'partner_revealed': False
        })
    # requesting user is first member, first member has not revealed and second member has
    elif convo.first_member_id is not None \
            and user.id == int(convo.first_member_id) \
            and convo.first_member_reveal == False \
            and convo.second_member_reveal == True:
        # print('Case 3')

        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': False,
            'partner_revealed': True
        })

    # requesting user is second, second member has revealed and partner hasnt
    elif (convo.second_member_id is not None
          and user.id == int(convo.second_member_id)) \
            and convo.second_member_reveal == True \
            and convo.first_member_reveal == False:
        # print('Case 4')

        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': True,
            'partner_revealed': False
        })
    # requesting user is second, second member has not revealed and partner has
    elif (convo.second_member_id is not None
          and user.id == int(convo.second_member_id)) \
            and convo.second_member_reveal == False \
            and convo.first_member_reveal == True:
        # print('Case 5')

        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': False,
            'partner_revealed': True
        })
    else:
        # IF NEITHER HAVE REVEALED
        # print('Case 6')

        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': False,
            'partner_revealed': False
        })


@api_view(['GET'])
def new_check_reveal_test(request, ):
    # takes convo id and checks if the user.id of the user making the request matches one of the member_ids
    # the match will only occur if the user has revealed their profile within the convo in question

    user = request.user
    convos = user.conversation.all()

    lst = []
    for convo in convos:
        # Both members have revealed
        if (convo.second_member_id is not None
                and convo.first_member_id is not None
                and convo.first_member_reveal == True
                and convo.second_member_reveal == True):
            # print('Case 1')
            lst.append({
                'user_id': user.id,
                'convo_id': convo.id,
                'revealed': True,
                'partner_revealed': True
            })

        # requesting user is first member, first member has revealed and partner hasnt
        elif convo.first_member_id is not None \
                and user.id == int(convo.first_member_id) \
                and convo.first_member_reveal == True \
                and convo.second_member_reveal == False:
            # print('Case 2')

            lst.append({
                'user_id': user.id,
                'convo_id': convo.id,
                'revealed': True,
                'partner_revealed': False
            })
        # requesting user is first member, first member has not revealed and second member has
        elif convo.first_member_id is not None \
                and user.id == int(convo.first_member_id) \
                and convo.first_member_reveal == False \
                and convo.second_member_reveal == True:
            # print('Case 3')

            lst.append({
                'user_id': user.id,
                'convo_id': convo.id,
                'revealed': False,
                'partner_revealed': True
            })


        # requesting user is second, second member has revealed and partner hasnt
        elif (convo.second_member_id is not None
              and user.id == int(convo.second_member_id)) \
                and convo.second_member_reveal == True \
                and convo.first_member_reveal == False:
            # print('Case 4')

            lst.append({
                'user_id': user.id,
                'convo_id': convo.id,
                'revealed': True,
                'partner_revealed': False
            })

        # requesting user is second, second member has not revealed and partner has
        elif (convo.second_member_id is not None
              and user.id == int(convo.second_member_id)) \
                and convo.second_member_reveal == False \
                and convo.first_member_reveal == True:
            # print('Case 5')

            lst.append({
                'user_id': user.id,
                'convo_id': convo.id,
                'revealed': False,
                'partner_revealed': True
            })
        else:
            # IF NEITHER HAVE REVEALED
            # print('Case 6')
            lst.append({
                'user_id': user.id,
                'convo_id': convo.id,
                'revealed': False,
                'partner_revealed': False
            })
    return Response(lst)


@api_view(['PATCH'])
def edit_profile(request):
    user = request.user
    data = request.data
    # create new dict containing only filled out fields of the edit form
    filtered_data = {}
    for (key, value) in data.items():
        if value != '' and value != None:
            filtered_data[key] = value

    # for when user is editing their existing profile
    if Profile.objects.filter(user=user).exists():
        profile = user.profile

    # for when user has just signed up and is adding profile details for the first time
    else:
        profile = Profile.objects.create(user=user)

    serializer = ProfileSerializer(instance=profile, data=filtered_data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response('Profile succefuly edited')
    return Response('Profile edit failed')


@api_view(['GET'])
def profile_check_on_first_signin(request):
    user = request.user
    if Profile.objects.filter(user=user).exists():
        return Response({'profile_filled_check': True})
    return Response({'profile_filled_check': False})


@api_view(['DELETE'])
def delete_convo(request, pk):
    convo = Conversation.objects.get(id=pk)
    convo.delete()
    return Response(f'Convo with id {pk} has been deleted')


@api_view(['GET'])
def create_new_chat(request):
    requesting_user = request.user
    # # list of all users excluding the requesting user (so the requesting user isn't matched to him/herself)
    all_users = list(User.objects.exclude(id=requesting_user.id))

    def generate_random_user():
        generated_user = random.choice(all_users)
        return generated_user

    # randomly select conversation partner
    random_user = generate_random_user()
    all_convos = requesting_user.conversation.all()
    # list containing all existing conversation partners of requesting user
    conversation_partner_list = []
    # loop through all of requesting users convos
    for convo in all_convos:
        # loop through all the members of those convos and append them to the list
        for member in convo.members.all().exclude(id=requesting_user.id):
            conversation_partner_list.append(member.username)
    # check if the randomly generated user is already in the list of requesting users convo partners
    random_user_passes_checks = False
    while random_user_passes_checks is False:
        if random_user.username in conversation_partner_list:
            # convo with previous randomly generated user exists, generate a new random user
            random_user = generate_random_user()
            # check if requesting user already has a convo open with all available users; if so, break to avoid
            # infinite loop
            if len(conversation_partner_list) == User.objects.all().count() - 1:
                break
        # if not in list, generate new convo
        else:
            convo = Conversation.objects.create(first_member_id=requesting_user.id,
                                                second_member_id=random_user.id,
                                                first_member_reveal=0,
                                                second_member_reveal=0,
                                                title=f'Conversation {Conversation.objects.last().id + 1}'
                                                )
            members = [requesting_user, random_user]
            convo.members.set(members)
            # break out of while loop after convo is created
            random_user_passes_checks = True
            return Response(
                [
                    {
                        'convo_id': convo.id,
                        'messages': None
                    }
                ]
            )
    return Response('New chat created')


# check if user is online
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    if Profile.objects.filter(user_id=user.id).exists():
        user.profile.is_online = True
        user.profile.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    if Profile.objects.filter(user_id=user.id).exists():
        user.profile.is_online = False
        user.profile.save()


@api_view(['POST'])
def demo_account_signin(request):
    params = {'username': 'demo_user', 'password': 'demo_password'}
    r = requests.post('https://drf-react-chat-backend.herokuapp.com/dj-rest-auth/signin/', json=params)
    if r.status_code == 200:
        response_dict = json.loads(r.text)
        return Response({'access_token': response_dict['access_token']})
    return Response('Could not save data')
