# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0003_auto_20170423_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 24, 0, 14, 42, 701793), verbose_name=b'Heure Arriv\xc3\xa9e'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='usager',
            unique_together=set([('nom', 'prenom')]),
        ),
    ]
