# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-20 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0011_auto_20170116_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='color',
            field=models.CharField(max_length=7),
        ),
    ]
