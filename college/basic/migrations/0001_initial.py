# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DateOfTable',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('create_time', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'date_of_table',
            },
        ),
        migrations.CreateModel(
            name='Fields',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('field_name', models.CharField(max_length=30)),
                ('field_name_cn', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'fields',
            },
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('table_name', models.CharField(max_length=30, unique=True)),
                ('table_name_cn', models.CharField(max_length=255, unique=True)),
                ('create_time', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'tables',
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('field_type', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'types',
            },
        ),
        migrations.AddField(
            model_name='fields',
            name='field_type',
            field=models.ForeignKey(related_name='Fields', to='basic.Types'),
        ),
        migrations.AddField(
            model_name='fields',
            name='table',
            field=models.ForeignKey(related_name='Fields', to='basic.Tables'),
        ),
        migrations.AddField(
            model_name='dateoftable',
            name='table',
            field=models.ForeignKey(related_name='DateOfTable', to='basic.Tables'),
        ),
    ]
