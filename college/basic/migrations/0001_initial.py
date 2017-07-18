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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'date_of_table',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('field_name', models.CharField(max_length=30)),
                ('field_name_cn', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'field',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('table_name', models.CharField(max_length=30, unique=True)),
                ('table_name_cn', models.CharField(max_length=255, unique=True)),
                ('create_time', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='TypeOfField',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('field_type', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'type_of_field',
            },
        ),
        migrations.CreateModel(
            name='TypeOfTable',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30, unique=True)),
                ('type', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'type_of_table',
            },
        ),
        migrations.CreateModel(
            name='YearAndMonth',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('year', models.IntegerField(null=True, blank=True)),
                ('month', models.IntegerField(null=True, blank=True)),
                ('type', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'year_and_month',
            },
        ),
        migrations.AddField(
            model_name='table',
            name='type',
            field=models.ForeignKey(related_name='Table', to='basic.TypeOfTable'),
        ),
        migrations.AddField(
            model_name='field',
            name='field_type',
            field=models.ForeignKey(related_name='Fields', to='basic.TypeOfField'),
        ),
        migrations.AddField(
            model_name='field',
            name='table',
            field=models.ForeignKey(related_name='Fields', to='basic.Table'),
        ),
        migrations.AddField(
            model_name='dateoftable',
            name='date',
            field=models.ForeignKey(related_name='DateOfTable', to='basic.YearAndMonth'),
        ),
        migrations.AddField(
            model_name='dateoftable',
            name='table',
            field=models.ForeignKey(related_name='DateOfTable', to='basic.Table'),
        ),
    ]
