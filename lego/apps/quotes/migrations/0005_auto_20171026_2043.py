# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 20:43
from __future__ import unicode_literals

from django.db import migrations

import lego.apps.content.fields


class Migration(migrations.Migration):

    dependencies = [("quotes", "0004_auto_20171026_2017")]

    operations = [
        migrations.AlterField(
            model_name="quote",
            name="text",
            field=lego.apps.content.fields.ContentField(allow_images=False),
        )
    ]
