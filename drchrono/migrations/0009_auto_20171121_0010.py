# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0008_auto_20171121_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='arrived_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='waiting_time',
            field=models.TimeField(null=True),
        ),
    ]
