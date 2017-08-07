# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0007_auto_20170804_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsAndCollege',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('college', models.ForeignKey(related_name='news_and_college', to='basic.College')),
            ],
            options={
                'db_table': 'news_and_college',
            },
        ),
        migrations.RemoveField(
            model_name='news',
            name='college_id_code',
        ),
        migrations.AddField(
            model_name='newsandcollege',
            name='news',
            field=models.ForeignKey(related_name='news_and_college', to='basic.News'),
        ),
        migrations.AddField(
            model_name='news',
            name='college',
            field=models.ManyToManyField(related_name='news', through='basic.NewsAndCollege', verbose_name='相关院校', to='basic.College'),
        ),
    ]
