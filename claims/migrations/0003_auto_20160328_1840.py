# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-28 18:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('claims', '0002_auto_20160328_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='user',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
