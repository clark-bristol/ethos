# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-09-05 14:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0010_rename'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claim',
            old_name='votes',
            new_name='affirmations',
        ),
        migrations.RenameField(
            model_name='claim',
            old_name='user_id',
            new_name='contrib_user_id',
        ),
        migrations.RenameField(
            model_name='claim',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='claim',
            name='source',
        ),
        migrations.RemoveField(
            model_name='claim',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='claim',
            name='user',
        ),
    ]