# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchOfTable',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=255, blank=True, null=True)),
                ('create_time', models.DateField(blank=True, null=True)),
                ('excel_file', models.FileField(blank=True, upload_to='data/excel', null=True)),
            ],
            options={
                'db_table': 'batch_of_table',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(unique=True, max_length=30, verbose_name='学校名称')),
                ('id_code', models.CharField(unique=True, max_length=30, verbose_name='学校标识码')),
                ('area', models.CharField(max_length=30, blank=True, null=True, verbose_name='片区')),
                ('province', models.CharField(max_length=30, blank=True, null=True, verbose_name='所在地（省级）')),
                ('city', models.CharField(max_length=30, blank=True, null=True, verbose_name='所在地（城市）')),
                ('nation_code', models.CharField(max_length=40, blank=True, null=True, verbose_name='行政区划编码')),
                ('is_vice_ministry', models.BooleanField(default=False, verbose_name='副部级高校')),
                ('is_211', models.BooleanField(default=False, verbose_name='211工程')),
                ('is_985', models.BooleanField(default=False, verbose_name='985工程')),
                ('is_985_platform', models.BooleanField(default=False, verbose_name='985平台')),
                ('is_double_first_class', models.BooleanField(default=False, verbose_name='双一流大学')),
                ('setup_time', models.DateField(blank=True, null=True, verbose_name='成立时间')),
                ('cancel_time', models.DateField(blank=True, null=True, verbose_name='注销时间')),
                ('note', models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='已撤销')),
                ('transfer_to', models.CharField(max_length=30, blank=True, null=True, verbose_name='合并后学校代码')),
            ],
            options={
                'db_table': 'college',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30, blank=True, null=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='EduClass',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30, blank=True, null=True)),
            ],
            options={
                'db_table': 'edu_class',
            },
        ),
        migrations.CreateModel(
            name='EduLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30, blank=True, null=True)),
            ],
            options={
                'db_table': 'edu_level',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, blank=True, null=True)),
                ('province', models.CharField(max_length=40, blank=True, null=True)),
                ('city', models.CharField(max_length=40, blank=True, null=True)),
                ('district', models.CharField(max_length=40, blank=True, null=True)),
                ('parent', models.CharField(max_length=40, blank=True, null=True)),
                ('lng', models.FloatField(default=0)),
                ('lat', models.FloatField(default=0)),
                ('geohash', models.CharField(max_length=40, blank=True, null=True)),
            ],
            options={
                'db_table': 'nation',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(unique=True, max_length=255)),
                ('keywords', models.CharField(max_length=100, blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('comment_count', models.IntegerField(default=0)),
                ('is_allow_comments', models.BooleanField(default=True)),
                ('is_stick_top', models.BooleanField(default=False)),
                ('is_bold', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
                ('publish_time', models.DateTimeField(blank=True, null=True)),
                ('college', models.ForeignKey(related_name='news', to='basic.College')),
            ],
            options={
                'db_table': 'news',
            },
        ),
        migrations.CreateModel(
            name='NewsAndTag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(related_name='news_and_tag', to='basic.News')),
            ],
            options={
                'db_table': 'news_and_tag',
            },
        ),
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('reply', models.IntegerField(blank=True, null=True)),
                ('news', models.ForeignKey(related_name='news_comment', to='basic.News')),
                ('user', models.ForeignKey(related_name='news_comment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'news_comment',
            },
        ),
        migrations.CreateModel(
            name='NewsTag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'news_tag',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=30)),
                ('name_cn', models.CharField(unique=True, max_length=255)),
                ('create_time', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='TypeOfField',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=30)),
                ('size', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'type_of_field',
            },
        ),
        migrations.CreateModel(
            name='TypeOfTable',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(unique=True, max_length=30)),
            ],
            options={
                'db_table': 'type_of_table',
            },
        ),
        migrations.CreateModel(
            name='YearSeasonMonth',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(blank=True, null=True)),
                ('season', models.IntegerField(blank=True, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('type', models.IntegerField(default=0)),
                ('text', models.CharField(max_length=30, blank=True, null=True)),
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
            model_name='newsandtag',
            name='tag',
            field=models.ForeignKey(related_name='news_and_tag', to='basic.NewsTag'),
        ),
        migrations.AddField(
            model_name='news',
            name='tag',
            field=models.ManyToManyField(related_name='news', through='basic.NewsAndTag', to='basic.NewsTag'),
        ),
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.ForeignKey(related_name='news', to=settings.AUTH_USER_MODEL),
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
            name='department',
            field=models.ForeignKey(to='basic.Department', verbose_name='主管部门', related_name='college'),
        ),
        migrations.AddField(
            model_name='college',
            name='edu_class',
            field=models.ForeignKey(to='basic.EduClass', verbose_name='类别', related_name='college'),
        ),
        migrations.AddField(
            model_name='college',
            name='edu_level',
            field=models.ForeignKey(to='basic.EduLevel', verbose_name='办学层次', related_name='college'),
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
