from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Conversation, Message, Profile
from drf_extra_fields.fields import Base64ImageField

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

class ProfileSerializer(serializers.ModelSerializer):
    real_avatar = Base64ImageField(required=False)
    avatar = Base64ImageField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'