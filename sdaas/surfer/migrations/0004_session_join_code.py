# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0003_auto_20161122_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='join_code',
            field=models.CharField(default=9001, max_length=16),
            preserve_default=False,
        ),
    ]
