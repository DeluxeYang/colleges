# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0005_auto_20170804_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='description',
        ),
        migrations.AddField(
            model_name='news',
            name='abstract',
            field=models.TextField(blank=True, null=True, verbose_name='摘要'),
        ),
        migrations.AlterField(
            model_name='news',
            name='college_id_code',
            field=models.CharField(max_length=30, blank=True, null=True, verbose_name='相关院校'),
        ),
        migrations.AlterField(
            model_name='news',
            name='keywords',
            field=models.CharField(max_length=100, blank=True, null=True, verbose_name='关键字'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=255, verbose_name='标题', unique=True),
        ),
    ]
