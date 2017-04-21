# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_emplye', models.CharField(max_length=30, verbose_name=b'Nom & Prenom')),
                ('fonction', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PieceId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typePiece', models.CharField(max_length=15, choices=[(b'passeport', b'passeport'), (b'cni', b'CNI'), (b'recepisse', b'recepisse'), (b'autre', b'autre carte')])),
                ('date_expiration', models.DateField(blank=True)),
                ('code', models.CharField(default=0, help_text=b"Pour autre,laisser '0'", max_length=60, verbose_name=b'Num\xc3\xa9ro ou code de la pi\xc3\xa8ce')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
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
                ('nom_usgr', models.CharField(max_length=50, verbose_name=b'Nom & Prenom')),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('telephone', models.IntegerField(null=True, blank=True)),
                ('piece', models.ForeignKey(to='Identification.PieceId')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_jour', models.DateField(auto_now=True, verbose_name=b'Date du Jour')),
                ('heur_arr', models.TimeField(verbose_name=b'Heure Arriv\xc3\xa9e')),
                ('heur_deprt', models.DateTimeField(verbose_name=b'Heure Depart')),
                ('type_visit', models.CharField(max_length=20, verbose_name=b'Objet de la Visite')),
                ('nbre', models.IntegerField(default=0)),
                ('service', models.ForeignKey(to='Identification.Service')),
                ('usager', models.ForeignKey(to='Identification.Usager')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='usager',
            name='services',
            field=models.ManyToManyField(to='Identification.Service', through='Identification.Visite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employe',
            name='service',
            field=models.ForeignKey(to='Identification.Service'),
            preserve_default=True,
        ),
    ]
