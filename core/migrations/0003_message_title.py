# Generated by Django 4.2.3 on 2023-07-23 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_message_options_remove_message_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
