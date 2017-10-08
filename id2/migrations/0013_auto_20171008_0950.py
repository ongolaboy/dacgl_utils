# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0012_auto_20170512_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=50, verbose_name=b'Nom')),
                ('prenom', models.CharField(default=b'', max_length=50, verbose_name=b'Prenoms')),
                ('sexe', models.CharField(default=b'H', max_length=5, choices=[(b'H', b'homme'), (b'F', b'femme')])),
                ('telephone', models.IntegerField(null=True, blank=True)),
                ('piece', models.ForeignKey(to='id2.PieceId')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=30, verbose_name=b'Nom structure')),
                ('adresse', models.TextField(verbose_name=b'Adresse physique')),
                ('description', models.TextField(verbose_name=b'Description sommaire')),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('telephone', models.IntegerField(null=True, blank=True)),
                ('site_web', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='employe',
            name='structure',
            field=models.ForeignKey(to='id2.Societe'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abonne',
            name='derniere_modif',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 8, 50, 35, 537996, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abonne',
            name='inscription',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 8, 50, 35, 537957, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='nom_serv',
            field=models.CharField(max_length=30, verbose_name=b'NOM'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 8, 50, 35, 537279, tzinfo=utc), verbose_name=b'Heure Arriv\xc3\xa9e', auto_now_add=True),
            preserve_default=True,
        ),
    ]
