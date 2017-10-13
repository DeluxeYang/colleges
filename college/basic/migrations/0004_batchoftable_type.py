# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_batchandcollegerelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchoftable',
            name='type',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
