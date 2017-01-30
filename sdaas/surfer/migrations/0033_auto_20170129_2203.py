# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-29 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0032_auto_20170129_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='state',
            field=models.IntegerField(choices=[(2, 'Committed'), (0, 'Initializing'), (4, 'Started'), (1, 'Initialized'), (3, 'Starting')], default=0),
        ),
        migrations.AlterField(
            model_name='controllerpart',
            name='category',
            field=models.IntegerField(choices=[(1, 'Controller'), (0, 'Communicator'), (2, 'Picker'), (3, 'Transitioner')]),
        ),
    ]