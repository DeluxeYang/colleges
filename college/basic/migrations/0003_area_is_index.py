# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='is_index',
            field=models.BooleanField(default=False),
        ),
    ]
