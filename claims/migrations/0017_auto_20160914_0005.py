# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 00:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('claims', '0016_auto_20160913_2355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='affirmation',
            old_name='affirmed_claim',
            new_name='affirmed_claim_id',
        ),
        migrations.RenameField(
            model_name='affirmation',
            old_name='affirming_user',
            new_name='affirming_user_id',
        ),
        migrations.RenameField(
            model_name='claim',
            old_name='contrib_user',
            new_name='contributing_user_id',
        ),
        migrations.AlterUniqueTogether(
            name='affirmation',
            unique_together=set([('affirmed_claim_id', 'affirming_user_id')]),
        ),
    ]
