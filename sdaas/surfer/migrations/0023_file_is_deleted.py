# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-23 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0022_auto_20170123_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]