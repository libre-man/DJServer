# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-10 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0004_session_join_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='start',
            field=models.DateTimeField(),
        ),
    ]