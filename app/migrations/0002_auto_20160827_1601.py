# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-27 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterField(
            model_name='match',
            name='team1_odds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='match',
            name='team2_odds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='match',
            name='valid',
            field=models.BooleanField(),
        ),
    ]
