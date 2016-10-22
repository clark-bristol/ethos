# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0024_auto_20161008_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('supported_claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supporting_arguments', to='claims.Claim')),
            ],
        ),
        migrations.CreateModel(
            name='ArgumentPremise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('argument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='claims.Argument')),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='claims.Claim')),
            ],
        ),
    ]