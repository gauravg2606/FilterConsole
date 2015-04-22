# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0003_auto_20150419_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
