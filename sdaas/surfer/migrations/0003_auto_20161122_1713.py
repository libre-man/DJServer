# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0002_joinedclient'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='color',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='url',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
    ]
