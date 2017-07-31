# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_auto_20170729_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='id_code',
            field=models.CharField(verbose_name='学校标识码', unique=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='college',
            name='name_cn',
            field=models.CharField(verbose_name='学校名称', unique=True, max_length=30),
        ),
    ]
