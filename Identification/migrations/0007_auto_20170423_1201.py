# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0006_auto_20170423_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visite',
            name='date_jour',
        ),
        migrations.AlterField(
            model_name='visite',
            name='heur_arr',
            field=models.TimeField(default=datetime.datetime(2017, 4, 23, 12, 1, 57, 261122), verbose_name=b'Heure Arriv\xc3\xa9e'),
            preserve_default=True,
        ),
    ]
