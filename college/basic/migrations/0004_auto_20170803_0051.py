# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_area_is_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='nation_code_2',
            field=models.CharField(max_length=2, blank=True, null=True),
        ),
    ]
