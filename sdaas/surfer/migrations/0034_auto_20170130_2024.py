# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-30 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0033_auto_20170129_2203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='url',
        ),
        migrations.RemoveField(
            model_name='session',
            name='start',
        ),
        migrations.AlterField(
            model_name='channel',
            name='state',
            field=models.IntegerField(choices=[(1, 'Initialized'), (3, 'Starting'), (4, 'Started'), (2, 'Committed'), (0, 'Initializing')], default=0),
        ),
        migrations.AlterField(
            model_name='controllerpart',
            name='category',
            field=models.IntegerField(choices=[(1, 'Controller'), (0, 'Communicator'), (3, 'Transitioner'), (2, 'Picker')]),
        ),
    ]
