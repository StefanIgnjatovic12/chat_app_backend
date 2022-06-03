from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Conversation, Message, Profile
from .serializers import ConversationSerializer, MessageSerializer, ProfileSerializer
import base64
import datetime


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
        key=lambda x:
        max(datetime.datetime.strptime(msg['created_on'], '%d.%m.%Y %H:%M:%S') for msg in x['messages']),
        reverse=True)
    return Response(sorted_data)


@api_view(['GET'])
def get_partner_and_last_message_from_user(request, pk):
    # Get conversation partner and last message from conversation
    # active user sending request
    user = User.objects.get(id=pk)
    # conversations belonging to active user
    conversations = user.conversation.all()
    conversation_list = []
    # loop through their conversation objects
    for conversation in conversations:
        # loop through members belonging to each conversation the active user is apart of
        for member in conversation.members.all():
            # if the member of the conversation isnt the active user its the convo partner
            if member != user:
                last_message = conversation.messages.last().message
                message_created_on = conversation.messages.last().created_on
                avatar = str(Profile.objects.get(user_id=member.id).avatar)
                # encode avatar img file as base64 to be rendered on front end
                with open(avatar, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                conversation_list.append(
                    {
                        'conv_id': conversation.id,
                        'conv_partner': member.username,
                        'last_message': last_message,
                        # 'created_on': message_created_on.strftime("%d.%m.%Y %H:%M"),
                        'created_on': message_created_on.strftime("%d.%m.%Y %H:%M:%S"),
                        'avatar': encoded_string,

                    }

                )
    sorted_data = sorted(conversation_list,
                         key=lambda x: datetime.datetime.strptime(x['created_on'], '%d.%m.%Y %H:%M:%S'),
                         reverse=True)
    return Response(sorted_data)


@api_view(['GET'])
def get_messages_with_user(request, pk, name):
    # currently active user which is sending the request
    active_user = User.objects.get(id=pk)
    # all convos belonging to that user
    conversations = active_user.conversation.all()
    conv_partner = User.objects.get(username=name)
    convo_partner_avatar = str(Profile.objects.get(user_id=conv_partner.id).avatar)
    # encode avatar img file as base64 to be rendered on front end
    with open(convo_partner_avatar, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    sorted_data = []
    # loop through all their conversation objects
    for convo in conversations:
        # loop through members of each conversation
        for member in convo.members.all():
            # match conversation partner to the name parameter passed
            if member.username == name:
                sorted_data.append(
                    {
                        'convo_id': convo.id,
                        'conv_partner': name,
                        'avatar': encoded_string,
                        # 'convo_partner': {
                        #     'name': name,
                        #     'avatar': encoded_string,
                        # },
                        'messages': [],
                        'last_message': convo.messages.last().message
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
    print(convo_id)
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
    with open(str(profile.avatar), "rb") as image_file:
        encoded_avatar = base64.b64encode(image_file.read())
    with open(str(profile.real_avatar), "rb") as image_file_2:
        encoded_real_avatar = base64.b64encode(image_file_2.read())
    return Response([{
        'age': profile.age,
        'gender': profile.gender,
        'location': profile.location,
        'description': profile.description,
        'interests': profile.interests,
        'reason': profile.reason,
        'real_name': profile.real_name,
        'avatar': encoded_avatar,
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
    print(f'requesting user: {user}, id: {user.id}')
    print(f'first member reveal: {convo.first_member_reveal}, second: {convo.second_member_reveal}')
    print(f'first member ID {convo.first_member_id}, second: {convo.second_member_id}')
    print(f'type of user id: {type(user.id)}, of member: {type(convo.first_member_id)}')
    # if neither conversation member has revealed, do it for the first member
    if convo.first_member_reveal == True and int(convo.first_member_id) == user.id:
        print('first scenario match')
        convo.first_member_reveal = False
        convo.save()
    elif convo.second_member_reveal == True and int(convo.second_member_id) == user.id:
        print('second scenario match')
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
                print(f'This is the member {member}')
                profile = Profile.objects.get(user_id=member.id)
                with open(str(profile.real_avatar), "rb") as image_file_2:
                    encoded_real_avatar = base64.b64encode(image_file_2.read())
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
    if convo.first_member_id is not None \
            and user.id == int(convo.first_member_id) \
            and convo.first_member_reveal == True:
        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': True
        })
        # return Response(f'Member with id {user.id} has revealed their profile in convo with id {convo.id}')
    elif (convo.second_member_id is not None
          and user.id == int(convo.second_member_id)) \
          and convo.second_member_reveal == True:
        # return Response(f'Member with id {user.id} has revealed their profile in convo with id {convo.id}')
        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': True
        })
    else:
        return Response({
            'user_id': user.id,
            'convo_id': convo.id,
            'revealed': False
        })


@api_view(['PATCH'])
def edit_profile(request):
    user = request.user
    data = request.data

    # create new dict containing only filled out fields of the edit form
    filtered_data = {}
    for (key, value) in data.items():
        if value != '':
            filtered_data[key] = value

    # for when user is editing their existing profile
    if Profile.objects.filter(user=user).exists():
        # if user.profile.exists():
        print('profile exists')
        profile = user.profile
    # for when user has just signed up and is adding profile details for the first time
    else:
        print('profile doesnt exist, creating profile')
        profile = Profile.objects.create(user=user)
        print(profile)

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
