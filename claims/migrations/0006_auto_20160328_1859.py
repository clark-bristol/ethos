# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-28 18:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0005_claim_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
