# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usager',
            name='sexe',
            field=models.CharField(default=b'H', max_length=5, choices=[(b'H', b'homme'), (b'F', b'femme')]),
            preserve_default=True,
        ),
    ]
