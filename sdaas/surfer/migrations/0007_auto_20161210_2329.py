# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-10 23:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0006_auto_20161210_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='created',
        ),
        migrations.RemoveField(
            model_name='client',
            name='last_modified',
        ),
        migrations.RemoveField(
            model_name='session',
            name='created',
        ),
        migrations.RemoveField(
            model_name='session',
            name='last_modified',
        ),
    ]