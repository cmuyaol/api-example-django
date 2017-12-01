# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0009_auto_20171121_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='access_token',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_id',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
