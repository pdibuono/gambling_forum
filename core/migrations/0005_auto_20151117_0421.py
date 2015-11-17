# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_reply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='reply',
            new_name='pick',
        ),
    ]
