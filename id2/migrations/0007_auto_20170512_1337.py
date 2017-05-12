# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('id2', '0006_auto_20170509_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abonne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matricule', models.CharField(default=0, help_text='Code g\xe9n\xe9r\xe9 suivant les r\xe8gles du service', unique=True, max_length=60, verbose_name="Identifiant de l'abonn\xe9")),
                ('photo', models.ImageField(upload_to=b'id2/photos/%Y/%m/%d')),
                ('inscription', models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 37, 3, 132614, tzinfo=utc), auto_now_add=True)),
                ('expiration', models.DateTimeField(null=True, blank=True)),
                ('derniere_modif', models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 37, 3, 132654, tzinfo=utc), auto_now=True)),
                ('service', models.ForeignKey(to='id2.Service')),
                ('usager', models.ForeignKey(to='id2.Usager')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='visite',
            name='date_arrivee',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 12, 37, 3, 131948, tzinfo=utc), verbose_name=b'Heure Arriv\xc3\xa9e', auto_now_add=True),
            preserve_default=True,
        ),
    ]
