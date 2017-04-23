# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Identification', '0003_auto_20170421_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visite',
            name='type_visit',
            field=models.TextField(default=b'AUF', max_length=20, verbose_name=b'Objet de la Visite'),
            preserve_default=True,
        ),
    ]
