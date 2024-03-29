# Generated by Django 4.0.4 on 2022-05-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_profile_real_avatar_profile_revealed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='revealed',
        ),
        migrations.AddField(
            model_name='conversation',
            name='first_member_reveal',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='second_member_reveal',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
