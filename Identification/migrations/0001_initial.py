# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_serv', models.CharField(max_length=30, verbose_name=b'Service')),
            ],
        ),
        migrations.CreateModel(
            name='Usager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_usgr', models.CharField(max_length=50, verbose_name=b'Nom & Prenom')),
                ('CNI', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.IntegerField()),
            ],
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
        ),
        migrations.AddField(
            model_name='usager',
            name='services',
            field=models.ManyToManyField(to='Identification.Service', through='Identification.Visite'),
        ),
        migrations.AddField(
            model_name='employe',
            name='service',
            field=models.ForeignKey(to='Identification.Service'),
        ),
    ]
