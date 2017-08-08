# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0009_newsimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='content',
            new_name='html_code',
        ),
        migrations.AddField(
            model_name='news',
            name='md_doc',
            field=models.TextField(null=True, verbose_name='内容', blank=True),
        ),
    ]
