# -*- coding: utf-8 -*-
# Generated by Django 1.9b1 on 2016-01-23 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transaction_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
    ]
