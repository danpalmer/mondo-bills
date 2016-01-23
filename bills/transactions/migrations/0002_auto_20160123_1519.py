# -*- coding: utf-8 -*-
# Generated by Django 1.9b1 on 2016-01-23 15:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo_url', models.URLField()),
                ('category', models.CharField(max_length=100)),
                ('mondo_group_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='decline_reason',
        ),
        migrations.AddField(
            model_name='transaction',
            name='mondo_created',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='merchant_group',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='transactions.MerchantGroup'),
            preserve_default=False,
        ),
    ]