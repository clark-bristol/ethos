# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 02:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0019_auto_20160914_0038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claim',
            old_name='user',
            new_name='creator',
        ),
    ]