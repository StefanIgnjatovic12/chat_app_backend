# Generated by Django 4.0.4 on 2022-05-20 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_conversation_first_member_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='first_member_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='second_member_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
