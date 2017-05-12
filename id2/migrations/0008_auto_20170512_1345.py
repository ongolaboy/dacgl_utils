# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0007_auto_20170512_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonne',
            name='derniere_modif',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 45, 27, 27091, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abonne',
            name='inscription',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 45, 27, 27052, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 45, 27, 26328, tzinfo=utc), verbose_name=b'Heure Arriv\xc3\xa9e', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='abonne',
            unique_together=set([('usager', 'service')]),
        ),
    ]
