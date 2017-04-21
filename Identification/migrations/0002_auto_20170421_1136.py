# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usager',
            name='email',
            field=models.EmailField(max_length=75),
            preserve_default=True,
        ),
    ]
