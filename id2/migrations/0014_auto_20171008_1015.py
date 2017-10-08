# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0013_auto_20171008_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='email',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abonne',
            name='derniere_modif',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 9, 15, 48, 131509, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abonne',
            name='inscription',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 9, 15, 48, 131469, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='nom_serv',
            field=models.CharField(max_length=30, verbose_name=b'Service'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 9, 15, 48, 130725, tzinfo=utc), verbose_name=b'Heure Arriv\xc3\xa9e', auto_now_add=True),
            preserve_default=True,
        ),
    ]
