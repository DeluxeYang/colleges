# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30)),
                ('nation_code_2', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'area',
            },
        ),
    ]
