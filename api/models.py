from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Conversation(models.Model):
    title = models.CharField(max_length=100, null=False, default='')
    members = models.ManyToManyField(User, related_name='conversation')
    first_member_reveal = models.BooleanField(default=False, null=True)
    second_member_reveal = models.BooleanField(default=False, null=True)
    def __str__(self):
        return self.title

class Message(models.Model):
    message = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='message', on_delete=models.CASCADE, null=True, blank=True)
    # senderID = models.CharField(max_length=500, null=True)
    # ownedByCurrentUser = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.message

class Profile(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    REASON_CHOICES = [
        ('To meet friends', 'To meet friends'),
        ('To kill time', 'To kill time'),
        ('To test out the chat app', 'To test out the chat app'),
        ('Other', 'Other')
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(upload_to='avatars')
    age = models.IntegerField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=100, null=True)
    location = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=500, null=True)
    interests = models.CharField(max_length=500, null=True)
    reason = models.CharField(choices=REASON_CHOICES, max_length=100, null=True)
    real_name = models.CharField(max_length=50, null=True)
    real_avatar = models.ImageField(upload_to='avatars', null=True)


    def __str__(self):
        return self.user.username
# > avatar
# >name
# >age
# >gender
# >location
# >description
# >interests
# >reason for using chat


# conversation = Conversation.objects.get(id=1)
# print(conversation.messages.all() > foreign key reverse
#message = Message.objects.get(id=1)
# print(message.conversation.all()
# user = User.objects.get(id=1)
# print(user.conversation.all()