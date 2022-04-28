from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

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
def get_conversations_from_user(request,pk):
    # get all conversations to which user belongs
    user = User.objects.get(id=pk)
    conversations = user.conversation.all()
    serialized = ConversationSerializer(conversations, many=True)
    return Response(serialized.data)

@api_view(['POST'])
def create_new_message(request):
    # runs every time a new message is sent in chat and creates a new entry in DB
    user = User.objects.get(id=1)
    conversation = Conversation.objects.get(id=1)
    # message_content = request.data['message_content']
    message = Message.objects.create(message=request.data,
                                     conversation=conversation,
                                     created_by=user
                                     )
    message.save()
    return Response("Message succesfuly saved")
