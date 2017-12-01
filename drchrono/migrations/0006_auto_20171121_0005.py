# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0005_auto_20171121_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='waiting_time',
            field=models.TimeField(),
        ),
    ]
