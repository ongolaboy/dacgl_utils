# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-22 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventaire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(default='Autre', help_text='Quel famille de produits ? ordi,imprimante', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='ensemble',
            name='intitule',
            field=models.CharField(default='Piece', max_length=200),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='nom',
            field=models.CharField(help_text='Mobilier,info,élec,...', max_length=200),
        ),
        migrations.AlterField(
            model_name='commande',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='ensemble',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='commande',
            unique_together=set([('section', 'numero')]),
        ),
        migrations.AddField(
            model_name='produit',
            name='famille',
            field=models.ForeignKey(default='Autre', on_delete=django.db.models.deletion.CASCADE, to='inventaire.Famille'),
        ),
    ]