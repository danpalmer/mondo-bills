# -*- coding: utf-8 -*-
# Generated by Django 1.9b1 on 2016-01-24 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_current_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='current_balance',
            field=models.IntegerField(default=0),
        ),
    ]
