# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0009_auto_20150420_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagtheme',
            name='tag',
            field=models.ForeignKey(default=1, to='taggie.Tag'),
            preserve_default=False,
        ),
    ]
