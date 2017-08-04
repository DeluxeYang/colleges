# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_auto_20170804_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(null=True, blank=True, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_allow_comments',
            field=models.BooleanField(default=True, verbose_name='允许评论'),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_bold',
            field=models.BooleanField(default=False, verbose_name='加粗'),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='已发布'),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_stick_top',
            field=models.BooleanField(default=False, verbose_name='置顶'),
        ),
        migrations.AlterField(
            model_name='news',
            name='tag',
            field=models.ManyToManyField(through='basic.NewsAndTag', verbose_name='标签', to='basic.NewsTag', related_name='news'),
        ),
    ]
