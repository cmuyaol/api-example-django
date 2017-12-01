# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='doctor_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
