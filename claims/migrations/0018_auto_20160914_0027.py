# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 00:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('claims', '0017_auto_20160914_0005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='affirmation',
            old_name='affirmed_claim_id',
            new_name='claim_id',
        ),
        migrations.RenameField(
            model_name='affirmation',
            old_name='affirming_user_id',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='claim',
            old_name='contributing_user_id',
            new_name='user_id',
        ),
        migrations.AlterUniqueTogether(
            name='affirmation',
            unique_together=set([('claim_id', 'user_id')]),
        ),
    ]