# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0002_usager_sexe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visite',
            name='nbre',
        ),
        migrations.AlterField(
            model_name='visite',
            name='heur_deprt',
            field=models.DateTimeField(verbose_name=b'Heure Depart', blank=True),
            preserve_default=True,
        ),
    ]
