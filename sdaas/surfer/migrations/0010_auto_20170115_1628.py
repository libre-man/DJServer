# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0009_channel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
