# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-28 13:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Claims',
            new_name='Claim',
        ),
    ]
