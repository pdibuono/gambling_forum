# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151117_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pick',
            old_name='title',
            new_name='sport',
        ),
    ]
