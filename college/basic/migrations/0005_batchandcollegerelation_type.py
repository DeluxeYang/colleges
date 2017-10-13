# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_batchoftable_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchandcollegerelation',
            name='type',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
