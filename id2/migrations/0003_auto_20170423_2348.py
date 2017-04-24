# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0002_auto_20170423_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pieceid',
            name='code',
            field=models.CharField(default=0, help_text=b"Pour autre,laisser '0'", unique=True, max_length=60, verbose_name=b'Num\xc3\xa9ro ou code de la pi\xc3\xa8ce'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 23, 48, 2, 86009), verbose_name=b'Heure Arriv\xc3\xa9e'),
            preserve_default=True,
        ),
    ]
