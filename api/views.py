from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Conversation, Message, Avatar
from .serializers import ConversationSerializer, MessageSerializer
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
    print(request.user)
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
            created_on = created_on.strftime("%d.%m.%Y %H:%M")
            message_list.append({
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
            max(datetime.datetime.strptime(msg['created_on'], '%d.%m.%Y %H:%M') for msg in x['messages']),
        reverse=True)
    return Response(sorted_data)




@api_view(['GET'])
def get_partner_and_last_message_from_user(request, pk):
    # Get conversation partner and last message from conversation
    user = User.objects.get(id=pk)
    conversations = user.conversation.all()
    conversation_list = []
    for conversation in conversations:
        for member in conversation.members.all():
            if member != user:
                last_message = conversation.messages.last().message
                message_created_on = conversation.messages.last().created_on
                avatar = str(Avatar.objects.get(user_id=member.id).avatar)
                # encode avatar img file as base64 to be rendered on front end
                with open(avatar, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                conversation_list.append(
                     {
                            'conv_partner': member.username,
                            'last_message': last_message,
                            'created_on': message_created_on.strftime("%d.%m.%Y %H:%M"),
                            'avatar': encoded_string

                     }

                )
    sorted_data = sorted(conversation_list, key=lambda x: datetime.datetime.strptime(x['created_on'], '%d.%m.%Y %H:%M'), reverse=True)
    return Response(sorted_data)

@api_view(['GET'])
def get_messages_with_user(request, pk, name):
    print(name)
    active_user = User.objects.get(id=pk)
    # convo_partner = data.name
    conversations = active_user.conversation.all()
    sorted_data = []
    for convo in conversations:
        for member in convo.members.all():
            if member.username == name:
                serialized_messages = MessageSerializer(convo.messages.all(), many=True).data
                for message in serialized_messages:
                    sorted_data.append(
                        {
                            'message': message['message'],
                            'created_by': message['created_by']
                        }
                    )
                return Response(sorted_data)

    # serialized = ConversationSerializer(conversations, many=True)
    # # for convo in serialized.data:
    # #     for member in convo['members']:
    # #         if member['username'] == 'John':
    # #             print(convo)
    # #             convo_object = Conversation.objects.get(id=convo['id'])
    # #             print(MessageSerializer(convo_object.messages.all()))
    # #             return Response(convo)
    # return Response('placeholder')


@api_view(['POST'])
def create_new_message(request):
    # runs every time a new message is sent in chat and creates a new entry in DB
    data = request.data
    userID = data['created_by']
    user = User.objects.get(id=userID)
    conversation = Conversation.objects.get(id=1)
    # message_content = request.data['message_content']

    print(data)
    message = Message.objects.create(message=data['message'],
                                     conversation=conversation,
                                     created_by=user,
                                     # senderID=data['senderID'],
                                     # # ownedByCurrentUser=data['ownedByCurrentUser']
                                     )
    # message.save()
    return Response("Message succesfuly saved")


@api_view(['GET'])
def get_current_user(request):
    user = request.user
    print(request)
    return Response([{
        'user': user.username,
        'id': user.id
    }])

