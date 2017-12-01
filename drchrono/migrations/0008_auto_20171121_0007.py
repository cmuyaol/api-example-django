# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0007_auto_20171121_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='waiting_time',
            field=models.TimeField(default=None),
        ),
    ]
