# Generated by Django 4.0.4 on 2022-05-16 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_profile_age_profile_description_profile_gender_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='age',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='description',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='reason',
        ),
    ]
