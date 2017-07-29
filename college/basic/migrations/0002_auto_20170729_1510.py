# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='cancel_time',
            field=models.DateField(null=True, blank=True, max_length=50, verbose_name='注销时间'),
        ),
        migrations.AlterField(
            model_name='college',
            name='setup_time',
            field=models.DateField(null=True, blank=True, max_length=50, verbose_name='成立时间'),
        ),
    ]
