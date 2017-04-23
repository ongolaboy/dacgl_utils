# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PieceId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typePiece', models.CharField(max_length=15, choices=[(b'passeport', b'passeport'), (b'cni', b'CNI'), (b'recepisse', b'recepisse'), (b'autre', b'autre carte')])),
                ('date_expiration', models.DateField(null=True, blank=True)),
                ('code', models.CharField(default=0, help_text=b"Pour autre,laisser '0'", max_length=60, verbose_name=b'Num\xc3\xa9ro ou code de la pi\xc3\xa8ce')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_serv', models.CharField(max_length=30, verbose_name=b'Service')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=50, verbose_name=b'Nom')),
                ('prenom', models.CharField(default=b'', max_length=50, verbose_name=b'Prenoms')),
                ('sexe', models.CharField(default=b'H', max_length=5, choices=[(b'H', b'homme'), (b'F', b'femme')])),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('telephone', models.IntegerField(null=True, blank=True)),
                ('piece', models.ForeignKey(to='id2.PieceId')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_arrivee', models.DateTimeField(default=datetime.datetime(2017, 4, 23, 16, 32, 43, 434553), verbose_name=b'Heure Arriv\xc3\xa9e')),
                ('date_deprt', models.DateTimeField(null=True, verbose_name=b'Heure Depart', blank=True)),
                ('type_visit', models.TextField(default=b'AUF', verbose_name=b'Objet de la Visite')),
                ('service', models.ForeignKey(to='id2.Service')),
                ('usager', models.ForeignKey(to='id2.Usager')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='usager',
            name='services',
            field=models.ManyToManyField(to='id2.Service', through='id2.Visite'),
            preserve_default=True,
        ),
    ]
