# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0027_auto_20161008_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='content',
            field=models.TextField(max_length=10000),
        ),
    ]
