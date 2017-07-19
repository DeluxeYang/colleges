# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BatchOfTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(null=True, max_length=255, blank=True)),
                ('create_time', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'batch_of_table',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30, verbose_name='学校名称')),
                ('id_code', models.CharField(max_length=30, verbose_name='学校标识码')),
                ('department', models.CharField(null=True, max_length=30, blank=True, verbose_name='主管部门')),
                ('area', models.CharField(null=True, max_length=30, blank=True, verbose_name='片区')),
                ('nation_code', models.CharField(null=True, max_length=40, blank=True, verbose_name='行政区划编码')),
                ('edu_level', models.CharField(null=True, max_length=30, blank=True, verbose_name='办学层次')),
                ('is_vice_ministry', models.BooleanField(default=False, verbose_name='副部级高校')),
                ('is_211', models.BooleanField(default=False, verbose_name='211工程')),
                ('is_985', models.BooleanField(default=False, verbose_name='985工程')),
                ('is_985_platform', models.BooleanField(default=False, verbose_name='985平台')),
                ('is_double_first_class', models.BooleanField(default=False, verbose_name='双一流大学')),
                ('setup_time', models.DateField(null=True, blank=True, verbose_name='成立时间')),
                ('cancel_time', models.DateField(null=True, blank=True, verbose_name='注销时间')),
                ('note', models.CharField(null=True, max_length=255, blank=True, verbose_name='备注')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='已注销')),
                ('transfer_to', models.CharField(null=True, max_length=30, blank=True, verbose_name='合并后学校代码')),
            ],
            options={
                'db_table': 'college',
            },
        ),
        migrations.CreateModel(
            name='EduClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'edu_class',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('name_cn', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'field',
            },
        ),
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(null=True, max_length=40, blank=True)),
                ('province', models.CharField(null=True, max_length=40, blank=True)),
                ('city', models.CharField(null=True, max_length=40, blank=True)),
                ('district', models.CharField(null=True, max_length=40, blank=True)),
                ('parent', models.CharField(null=True, max_length=40, blank=True)),
                ('lng', models.FloatField(default=0)),
                ('lat', models.FloatField(default=0)),
                ('geohash', models.CharField(null=True, max_length=40, blank=True)),
            ],
            options={
                'db_table': 'nation',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('name_cn', models.CharField(max_length=255, unique=True)),
                ('create_time', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='TypeOfField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('size', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'type_of_field',
            },
        ),
        migrations.CreateModel(
            name='TypeOfTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'type_of_table',
            },
        ),
        migrations.CreateModel(
            name='YearSeasonMonth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(null=True, blank=True)),
                ('season', models.IntegerField(null=True, blank=True)),
                ('month', models.IntegerField(null=True, blank=True)),
                ('type', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'year_season_month',
            },
        ),
        migrations.AddField(
            model_name='table',
            name='type',
            field=models.ForeignKey(to='basic.TypeOfTable', related_name='Table'),
        ),
        migrations.AddField(
            model_name='field',
            name='table',
            field=models.ForeignKey(to='basic.Table', related_name='Fields'),
        ),
        migrations.AddField(
            model_name='field',
            name='type',
            field=models.ForeignKey(to='basic.TypeOfField', related_name='Fields'),
        ),
        migrations.AddField(
            model_name='college',
            name='edu_class',
            field=models.ForeignKey(to='basic.EduClass', related_name='college', verbose_name='类别'),
        ),
        migrations.AddField(
            model_name='batchoftable',
            name='batch',
            field=models.ForeignKey(to='basic.YearSeasonMonth', related_name='BatchOfTable'),
        ),
        migrations.AddField(
            model_name='batchoftable',
            name='table',
            field=models.ForeignKey(to='basic.Table', related_name='BatchOfTable'),
        ),
    ]
