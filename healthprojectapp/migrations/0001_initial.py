# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='health',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=10)),
                ('temperature', models.FloatField(max_length=4)),
                ('pulse', models.FloatField(max_length=4)),
            ],
        ),
    ]
