# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-28 18:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0003_auto_20160328_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='user_id',
        ),
    ]
