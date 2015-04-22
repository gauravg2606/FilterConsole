# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0011_tagtypes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TagTypes',
            new_name='TagType',
        ),
    ]
