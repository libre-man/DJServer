# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfer', '0010_auto_20170115_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='name',
        ),
        migrations.AddField(
            model_name='client',
            name='gender',
            field=models.CharField(default='m', max_length=1),
            preserve_default=False,
        ),
    ]