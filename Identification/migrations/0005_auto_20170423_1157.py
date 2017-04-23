# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0004_auto_20170421_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pieceid',
            name='date_expiration',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visite',
            name='heur_deprt',
            field=models.DateTimeField(null=True, verbose_name=b'Heure Depart', blank=True),
            preserve_default=True,
        ),
    ]
