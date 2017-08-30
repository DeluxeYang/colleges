# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchoftable',
            name='name_cn',
            field=models.CharField(max_length=255, unique=True, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='college',
            field=models.ManyToManyField(verbose_name='相关院校', through='basic.NewsAndCollege', to='basic.College'),
        ),
        migrations.AlterField(
            model_name='news',
            name='tag',
            field=models.ManyToManyField(verbose_name='标签', through='basic.NewsAndTag', to='basic.NewsTag'),
        ),
        migrations.AlterField(
            model_name='newsimage',
            name='image',
            field=models.ImageField(upload_to='news/images/'),
        ),
    ]
