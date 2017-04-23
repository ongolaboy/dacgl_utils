# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0007_auto_20170423_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visite',
            name='heur_arr',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 12, 2, 57, 250966), verbose_name=b'Heure Arriv\xc3\xa9e'),
            preserve_default=True,
        ),
    ]
