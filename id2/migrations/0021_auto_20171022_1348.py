# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-22 12:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0020_auto_20171022_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonne',
            name='derniere_modif',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 22, 12, 48, 47, 155740, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='abonne',
            name='inscription',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 22, 12, 48, 47, 155694, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 22, 12, 48, 47, 154307, tzinfo=utc), verbose_name='Heure Arrivée'),
        ),
        migrations.AlterField(
            model_name='visiteprof',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 22, 12, 48, 47, 154879, tzinfo=utc), verbose_name='Heure Arrivée'),
        ),
    ]
