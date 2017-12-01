# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0006_auto_20171121_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='arrived_time',
            field=models.DateTimeField(default=None),
        ),
    ]
