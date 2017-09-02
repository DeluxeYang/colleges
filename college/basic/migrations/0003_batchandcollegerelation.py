# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_auto_20170829_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchAndCollegeRelation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('batch', models.ForeignKey(related_name='BatchAndCollegeRelation', to='basic.BatchOfTable')),
                ('college', models.ForeignKey(related_name='BatchAndCollegeRelation', to='basic.College')),
            ],
            options={
                'db_table': 'batch_and_college',
            },
        ),
    ]
