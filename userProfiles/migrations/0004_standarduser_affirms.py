# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-18 00:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0009_claim_tags'),
        ('userProfiles', '0003_auto_20160329_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='standarduser',
            name='affirms',
            field=models.ManyToManyField(to='claims.Claim'),
        ),
    ]
