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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name_cn', models.CharField(max_length=255, blank=True, null=True)),
                ('create_time', models.DateField(blank=True, null=True)),
                ('excel_file', models.FileField(upload_to='data/excel', blank=True, null=True)),
            ],
            options={
                'db_table': 'batch_of_table',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name_cn', models.CharField(verbose_name='学校名称', max_length=30)),
                ('id_code', models.CharField(verbose_name='学校标识码', max_length=30)),
                ('department', models.CharField(verbose_name='主管部门', max_length=30, blank=True, null=True)),
                ('area', models.CharField(verbose_name='片区', max_length=30, blank=True, null=True)),
                ('nation_code', models.CharField(verbose_name='行政区划编码', max_length=40, blank=True, null=True)),
                ('edu_level', models.CharField(verbose_name='办学层次', max_length=30, blank=True, null=True)),
                ('is_vice_ministry', models.BooleanField(verbose_name='副部级高校', default=False)),
                ('is_211', models.BooleanField(verbose_name='211工程', default=False)),
                ('is_985', models.BooleanField(verbose_name='985工程', default=False)),
                ('is_985_platform', models.BooleanField(verbose_name='985平台', default=False)),
                ('is_double_first_class', models.BooleanField(verbose_name='双一流大学', default=False)),
                ('setup_time', models.DateField(verbose_name='成立时间', blank=True, null=True)),
                ('cancel_time', models.DateField(verbose_name='注销时间', blank=True, null=True)),
                ('note', models.CharField(verbose_name='备注', max_length=255, blank=True, null=True)),
                ('is_cancelled', models.BooleanField(verbose_name='已注销', default=False)),
                ('transfer_to', models.CharField(verbose_name='合并后学校代码', max_length=30, blank=True, null=True)),
            ],
            options={
                'db_table': 'college',
            },
        ),
        migrations.CreateModel(
            name='EduClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name_cn', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'edu_class',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('keywords', models.CharField(max_length=100, blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('comment_count', models.IntegerField(blank=True, null=True)),
                ('is_allow_comments', models.BooleanField(default=False)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('news', models.ForeignKey(related_name='news_and_tag', to='basic.News')),
            ],
            options={
                'db_table': 'news_and_tag',
            },
        ),
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'news_tag',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('name_cn', models.CharField(max_length=255, unique=True)),
                ('create_time', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='TypeOfField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('size', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'type_of_field',
            },
        ),
        migrations.CreateModel(
            name='TypeOfTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name_cn', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'type_of_table',
            },
        ),
        migrations.CreateModel(
            name='YearSeasonMonth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
            field=models.ManyToManyField(to='basic.NewsTag', related_name='news', through='basic.NewsAndTag'),
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
            name='edu_class',
            field=models.ForeignKey(verbose_name='类别', to='basic.EduClass', related_name='college'),
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
