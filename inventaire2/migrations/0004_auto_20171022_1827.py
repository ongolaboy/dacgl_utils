# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-22 17:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventaire2', '0003_auto_20171022_1822'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='salle',
            unique_together=set([('nom', 'site')]),
        ),
    ]
