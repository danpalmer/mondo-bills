# -*- coding: utf-8 -*-
# Generated by Django 1.9b1 on 2016-01-24 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recurring', '0002_auto_20160124_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringtransaction',
            name='is_subscription',
            field=models.BooleanField(default=True),
        ),
    ]