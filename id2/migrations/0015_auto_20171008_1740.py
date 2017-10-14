# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0014_auto_20171008_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisiteProf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_arrivee', models.DateTimeField(default=datetime.datetime(2017, 10, 8, 16, 40, 21, 202685, tzinfo=utc), verbose_name=b'Heure Arriv\xc3\xa9e', auto_now_add=True)),
                ('date_deprt', models.DateTimeField(null=True, verbose_name=b'Heure Depart', blank=True)),
                ('type_visit', models.TextField(default=b'Courrier', verbose_name=b'Objet de la Visite')),
                ('employe', models.ForeignKey(to='id2.Employe')),
                ('service', models.ForeignKey(to='id2.Service')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='abonne',
            name='derniere_modif',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 16, 40, 21, 203487, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abonne',
            name='inscription',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 16, 40, 21, 203450, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 16, 40, 21, 202177, tzinfo=utc), verbose_name=b'Heure Arriv\xc3\xa9e', auto_now_add=True),
            preserve_default=True,
        ),
    ]
