# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 01:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0021_auto_20160918_0215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='claim',
            name='content',
            field=models.CharField(default='', max_length=10000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='claim',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='claim',
            name='creator_user',
        ),
        migrations.AlterUniqueTogether(
            name='claim',
            unique_together=set([('name', 'content')]),
        ),
        migrations.AddField(
            model_name='argument',
            name='premise_claims',
            field=models.ManyToManyField(related_name='dependent_arguments', to='claims.Claim'),
        ),
        migrations.AddField(
            model_name='argument',
            name='supported_claim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supporting_arguments', to='claims.Claim'),
        ),
    ]
