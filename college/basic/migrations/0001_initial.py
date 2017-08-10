# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30)),
                ('nation_code_2', models.CharField(null=True, max_length=2, blank=True)),
                ('is_index', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='BatchOfTable',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(null=True, max_length=255, blank=True)),
                ('create_time', models.DateField(null=True, blank=True)),
                ('excel_file', models.FileField(upload_to='data/excel', null=True, blank=True)),
            ],
            options={
                'db_table': 'batch_of_table',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(verbose_name='学校名称', max_length=30, unique=True)),
                ('id_code', models.CharField(verbose_name='学校标识码', max_length=30, unique=True)),
                ('area', models.CharField(null=True, verbose_name='片区', max_length=30, blank=True)),
                ('province', models.CharField(null=True, verbose_name='所在地（省级）', max_length=30, blank=True)),
                ('city', models.CharField(null=True, verbose_name='所在地（城市）', max_length=30, blank=True)),
                ('nation_code', models.CharField(null=True, verbose_name='行政区划编码', max_length=40, blank=True)),
                ('is_vice_ministry', models.BooleanField(default=False, verbose_name='副部级高校')),
                ('is_211', models.BooleanField(default=False, verbose_name='211工程')),
                ('is_985', models.BooleanField(default=False, verbose_name='985工程')),
                ('is_985_platform', models.BooleanField(default=False, verbose_name='985平台')),
                ('is_double_first_class', models.BooleanField(default=False, verbose_name='双一流大学')),
                ('setup_time', models.DateField(null=True, verbose_name='成立时间', blank=True)),
                ('cancel_time', models.DateField(null=True, verbose_name='注销时间', blank=True)),
                ('note', models.CharField(null=True, verbose_name='备注', max_length=255, blank=True)),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='已撤销')),
                ('transfer_to', models.CharField(null=True, verbose_name='合并后学校代码', max_length=30, blank=True)),
            ],
            options={
                'db_table': 'college',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(null=True, max_length=30, blank=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='EduClass',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(null=True, max_length=30, blank=True)),
            ],
            options={
                'db_table': 'edu_class',
            },
        ),
        migrations.CreateModel(
            name='EduLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(null=True, max_length=30, blank=True)),
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
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='标题', max_length=255)),
                ('keywords', models.CharField(null=True, verbose_name='关键字', max_length=100, blank=True)),
                ('abstract', models.TextField(null=True, verbose_name='摘要', blank=True)),
                ('content', DjangoUeditor.models.UEditorField(default='', verbose_name='内容', blank=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='已发布')),
                ('is_allow_comments', models.BooleanField(default=True, verbose_name='允许评论')),
                ('is_stick_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('is_bold', models.BooleanField(default=False, verbose_name='加粗')),
                ('create_time', models.DateTimeField(null=True, blank=True)),
                ('update_time', models.DateTimeField(null=True, blank=True)),
                ('publish_time', models.DateTimeField(null=True, blank=True)),
                ('comment_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'news',
            },
        ),
        migrations.CreateModel(
            name='NewsAndCollege',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('college', models.ForeignKey(related_name='news_and_college', to='basic.College')),
                ('news', models.ForeignKey(related_name='news_and_college', to='basic.News')),
            ],
            options={
                'db_table': 'news_and_college',
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
                ('content', models.TextField(null=True, blank=True)),
                ('reply', models.IntegerField(null=True, blank=True)),
                ('news', models.ForeignKey(related_name='news_comment', to='basic.News')),
                ('user', models.ForeignKey(related_name='news_comment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'news_comment',
            },
        ),
        migrations.CreateModel(
            name='NewsImage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='news/photos/%Y/%m/%d')),
            ],
            options={
                'db_table': 'news_image',
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('size', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'type_of_field',
            },
        ),
        migrations.CreateModel(
            name='TypeOfTable',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'type_of_table',
            },
        ),
        migrations.CreateModel(
            name='YearSeasonMonth',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(null=True, blank=True)),
                ('season', models.IntegerField(null=True, blank=True)),
                ('month', models.IntegerField(null=True, blank=True)),
                ('type', models.IntegerField(default=0)),
                ('text', models.CharField(null=True, max_length=30, blank=True)),
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
            name='college',
            field=models.ManyToManyField(to='basic.College', verbose_name='相关院校', through='basic.NewsAndCollege', related_name='news'),
        ),
        migrations.AddField(
            model_name='news',
            name='tag',
            field=models.ManyToManyField(to='basic.NewsTag', verbose_name='标签', through='basic.NewsAndTag', related_name='news'),
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
            field=models.ForeignKey(to='basic.Department', related_name='college', verbose_name='主管部门'),
        ),
        migrations.AddField(
            model_name='college',
            name='edu_class',
            field=models.ForeignKey(to='basic.EduClass', related_name='college', verbose_name='类别'),
        ),
        migrations.AddField(
            model_name='college',
            name='edu_level',
            field=models.ForeignKey(to='basic.EduLevel', related_name='college', verbose_name='办学层次'),
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
