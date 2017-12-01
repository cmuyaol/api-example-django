# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0004_auto_20171121_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='arrived_time',
            field=models.DateTimeField(),
        ),
    ]
