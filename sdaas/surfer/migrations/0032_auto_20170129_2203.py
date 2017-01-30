# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-29 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0031_auto_20170129_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='end',
        ),
        migrations.AlterField(
            model_name='channel',
            name='state',
            field=models.IntegerField(choices=[(4, 'Started'), (0, 'Initializing'), (2, 'Committed'), (3, 'Starting'), (1, 'Initialized')], default=0),
        ),
        migrations.AlterField(
            model_name='controllerpart',
            name='category',
            field=models.IntegerField(choices=[(0, 'Communicator'), (1, 'Controller'), (2, 'Picker'), (3, 'Transitioner')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='start',
            field=models.DateTimeField(null=True),
        ),
    ]