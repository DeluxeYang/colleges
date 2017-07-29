# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_auto_20170729_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='cancel_time',
            field=models.DateField(verbose_name='注销时间', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='college',
            name='setup_time',
            field=models.DateField(verbose_name='成立时间', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='name_cn',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='educlass',
            name='name_cn',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='edulevel',
            name='name_cn',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
