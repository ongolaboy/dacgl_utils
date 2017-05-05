# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0004_auto_20170424_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Heure Arriv\xc3\xa9e'),
            preserve_default=True,
        ),
    ]
