# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-01 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0023_auto_20171031_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pieceid',
            name='code',
            field=models.CharField(blank=True, default=0, help_text="Pour autre,laisser '0'", max_length=60, verbose_name='Numéro ou code de la pièce'),
        ),
    ]
