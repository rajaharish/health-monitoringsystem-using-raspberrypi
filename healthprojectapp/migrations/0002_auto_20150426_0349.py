# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthprojectapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='health',
            name='timestamp',
            field=models.DateTimeField(max_length=10),
        ),
    ]
