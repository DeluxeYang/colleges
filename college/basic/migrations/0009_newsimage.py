# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0008_auto_20170805_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='news/photos/%Y/%m/%d')),
            ],
            options={
                'db_table': 'news_image',
            },
        ),
    ]
