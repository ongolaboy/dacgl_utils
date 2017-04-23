# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0005_auto_20170423_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visite',
            name='date_jour',
            field=models.DateField(default=datetime.datetime(2017, 4, 23, 11, 59, 54, 971890), verbose_name=b'Date du Jour'),
            preserve_default=True,
        ),
    ]
