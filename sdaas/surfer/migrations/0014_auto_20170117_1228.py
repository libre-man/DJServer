# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0013_auto_20170117_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controllerpart',
            name='category',
            field=models.IntegerField(choices=[(0, 'Communicator'), (3, 'Transitioner'), (2, 'Picker'), (1, 'Controller')]),
        ),
    ]
