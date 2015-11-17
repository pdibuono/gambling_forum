# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='reply',
            field=models.ForeignKey(blank=True, to='core.Reply', null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='pick',
            field=models.ForeignKey(blank=True, to='core.Pick', null=True),
        ),
    ]
