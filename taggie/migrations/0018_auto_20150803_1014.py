# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0017_sticker_time'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TagTheme',
            new_name='TypesToTag',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='theme',
            new_name='tagtype',
        ),
    ]
