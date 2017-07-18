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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name_cn', models.CharField(null=True, max_length=255, blank=True)),
            ],
            options={
                'db_table': 'batch_of_table',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name_cn', models.CharField(verbose_name='学校名称', max_length=30)),
                ('id_code', models.CharField(verbose_name='学校标识码', max_length=30)),
                ('department', models.CharField(verbose_name='主管部门', null=True, max_length=30, blank=True)),
                ('area', models.CharField(verbose_name='片区', null=True, max_length=30, blank=True)),
                ('nation_code', models.CharField(verbose_name='行政区划编码', null=True, max_length=40, blank=True)),
                ('edu_level', models.CharField(verbose_name='办学层次', null=True, max_length=30, blank=True)),
                ('is_vice_ministry', models.BooleanField(verbose_name='副部级高校', default=False)),
                ('is_211', models.BooleanField(verbose_name='211工程', default=False)),
                ('is_985', models.BooleanField(verbose_name='985工程', default=False)),
                ('is_985_platform', models.BooleanField(verbose_name='985平台', default=False)),
                ('is_double_first_class', models.BooleanField(verbose_name='双一流大学', default=False)),
                ('setup_time', models.DateField(verbose_name='成立时间', null=True, blank=True)),
                ('cancel_time', models.DateField(verbose_name='注销时间', null=True, blank=True)),
                ('note', models.CharField(verbose_name='备注', null=True, max_length=255, blank=True)),
                ('is_cancelled', models.BooleanField(verbose_name='已注销', default=False)),
                ('transfer_to', models.CharField(verbose_name='合并后学校代码', null=True, max_length=30, blank=True)),
            ],
            options={
                'db_table': 'college',
            },
        ),
        migrations.CreateModel(
            name='EduClass',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name_cn', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'edu_class',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('name_cn', models.CharField(unique=True, max_length=255)),
                ('create_time', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='TypeOfField',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name_cn', models.CharField(unique=True, max_length=30)),
            ],
            options={
                'db_table': 'type_of_table',
            },
        ),
        migrations.CreateModel(
            name='YearSeasonMonth',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
            field=models.ForeignKey(related_name='Table', to='basic.TypeOfTable'),
        ),
        migrations.AddField(
            model_name='field',
            name='table',
            field=models.ForeignKey(related_name='Fields', to='basic.Table'),
        ),
        migrations.AddField(
            model_name='field',
            name='type',
            field=models.ForeignKey(related_name='Fields', to='basic.TypeOfField'),
        ),
        migrations.AddField(
            model_name='college',
            name='edu_class',
            field=models.ForeignKey(to='basic.EduClass', verbose_name='类别', related_name='college'),
        ),
        migrations.AddField(
            model_name='batchoftable',
            name='batch',
            field=models.ForeignKey(related_name='BatchOfTable', to='basic.YearSeasonMonth'),
        ),
        migrations.AddField(
            model_name='batchoftable',
            name='table',
            field=models.ForeignKey(related_name='BatchOfTable', to='basic.Table'),
        ),
    ]
