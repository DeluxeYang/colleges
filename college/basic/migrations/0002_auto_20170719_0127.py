# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchoftable',
            name='create_time',
            field=models.DateField(null=True, blank=True),
        ),
    ]
