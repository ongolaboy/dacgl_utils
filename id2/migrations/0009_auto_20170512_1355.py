# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0008_auto_20170512_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonne',
            name='derniere_modif',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 55, 20, 293535, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abonne',
            name='expiration',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abonne',
            name='inscription',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 55, 20, 293495, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 55, 20, 292693, tzinfo=utc), verbose_name=b'Heure Arriv\xc3\xa9e', auto_now_add=True),
            preserve_default=True,
        ),
    ]
