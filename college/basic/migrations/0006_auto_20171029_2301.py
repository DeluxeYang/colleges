# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 15:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0005_auto_20171029_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='table',
        ),
        migrations.RemoveField(
            model_name='professorandcollegerelation',
            name='type',
        ),
        migrations.RemoveField(
            model_name='ranking',
            name='table',
        ),
        migrations.RemoveField(
            model_name='rankingandcollegerelation',
            name='type',
        ),
    ]
