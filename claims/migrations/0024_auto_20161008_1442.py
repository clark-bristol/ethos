# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 14:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0023_auto_20161008_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='argument',
            name='supported_claim',
        ),
        migrations.RemoveField(
            model_name='argumentpremise',
            name='argument',
        ),
        migrations.RemoveField(
            model_name='argumentpremise',
            name='claim',
        ),
        migrations.DeleteModel(
            name='Argument',
        ),
        migrations.DeleteModel(
            name='ArgumentPremise',
        ),
    ]