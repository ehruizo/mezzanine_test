# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-21 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbtest', '0003_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='invoice',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Invoice number'),
        ),
    ]
