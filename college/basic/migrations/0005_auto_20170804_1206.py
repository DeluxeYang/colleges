# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_auto_20170803_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='college',
        ),
        migrations.AddField(
            model_name='news',
            name='college_id_code',
            field=models.CharField(max_length=30, blank=True, null=True),
        ),
    ]
