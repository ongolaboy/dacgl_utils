# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0009_auto_20170423_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employe',
            name='service',
        ),
        migrations.DeleteModel(
            name='Employe',
        ),
        migrations.AlterField(
            model_name='visite',
            name='heur_arr',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 15, 9, 53, 347509), verbose_name=b'Heure Arriv\xc3\xa9e'),
            preserve_default=True,
        ),
    ]
