# Generated by Django 5.0.4 on 2024-06-11 15:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0013_roomshare'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentreply',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 6, 11, 15, 28, 3, 389460, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commentreply',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='roomcomment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 6, 11, 15, 29, 14, 876197, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roomcomment',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
