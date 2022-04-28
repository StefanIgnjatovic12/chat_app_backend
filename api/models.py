from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Conversation(models.Model):
    title = models.CharField(max_length=100, null=False, default='')
    members = models.ManyToManyField(User, related_name='conversation')



class Message(models.Model):
    message = models.CharField(max_length=500)
    created_on = models.TimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='message', on_delete=models.CASCADE, null=True, blank=True)



# conversation = Conversation.objects.get(id=1)
# print(conversation.messages.all() > foreign key reverse
#message = Message.objects.get(id=1)
# print(message.conversation.all()
# user = User.objects.get(id=1)
# print(user.conversation.all()
