# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-01 17:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0024_auto_20171101_1653'),
        ('manif', '0002_evenement_ouvert'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('usager', 'evenement')]),
        ),
    ]
