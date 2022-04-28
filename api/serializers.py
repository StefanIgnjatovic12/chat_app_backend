from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Conversation, Message
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ConversationSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer(many=False)

    class Meta:
        model = Message
        fields = '__all__'