# Generated by Django 4.0.1 on 2022-01-26 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0004_alter_chats_receive_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='img',
            field=models.ImageField(null=True, upload_to='Chats/'),
        ),
    ]