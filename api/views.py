from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Conversation, Message, Avatar
from .serializers import ConversationSerializer, MessageSerializer
import base64


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
            message_list.append({
                'message': message['message'],
                'created_on': message['created_on'],
                'created_by': message['created_by']
            })
            convo['messages'] = message_list
        # clear the list so that each conversation is attached only its own messages
        message_list = []
    # print(lst)
    return Response(serialized_convos.data)




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

    return Response(conversation_list)


@api_view(['POST'])
def create_new_message(request):
    # runs every time a new message is sent in chat and creates a new entry in DB
    user = User.objects.get(id=1)
    conversation = Conversation.objects.get(id=1)
    # message_content = request.data['message_content']
    data = request.data
    print(data)
    message = Message.objects.create(message=data['message'],
                                     conversation=conversation,
                                     created_by=user,
                                     senderID=data['senderID'],
                                     ownedByCurrentUser=data['ownedByCurrentUser']
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

