# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0016_langtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='sticker',
            name='time',
            field=models.IntegerField(default=-1),
        ),
    ]
