from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Conversation(models.Model):
    title = models.CharField(max_length=100, null=False, default='')
    members = models.ManyToManyField(User, related_name='conversation')

    def __str__(self):
        return self.title

class Message(models.Model):
    message = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='message', on_delete=models.CASCADE, null=True, blank=True)
    senderID = models.CharField(max_length=500, null=True)
    ownedByCurrentUser = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.message

class Avatar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(upload_to='avatars')


# conversation = Conversation.objects.get(id=1)
# print(conversation.messages.all() > foreign key reverse
#message = Message.objects.get(id=1)
# print(message.conversation.all()
# user = User.objects.get(id=1)
# print(user.conversation.all()
