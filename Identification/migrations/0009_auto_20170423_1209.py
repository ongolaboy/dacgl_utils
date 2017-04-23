# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0008_auto_20170423_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visite',
            name='heur_arr',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 12, 9, 55, 309764), verbose_name=b'Heure Arriv\xc3\xa9e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visite',
            name='type_visit',
            field=models.TextField(default=b'AUF', verbose_name=b'Objet de la Visite'),
            preserve_default=True,
        ),
    ]
