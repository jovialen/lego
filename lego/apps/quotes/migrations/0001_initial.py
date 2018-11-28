# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 10:20
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tags", "0001_initial"),
        ("files", "0002_file_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "deleted",
                    models.BooleanField(db_index=True, default=False, editable=False),
                ),
                ("slug", models.SlugField(null=True, unique=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("text", models.TextField(blank=True)),
                ("source", models.CharField(max_length=255)),
                ("approved", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=None,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quote_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("images", models.ManyToManyField(blank=True, to="files.File")),
                ("tags", models.ManyToManyField(blank=True, to="tags.Tag")),
                (
                    "updated_by",
                    models.ForeignKey(
                        default=None,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quote_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False, "default_manager_name": "objects"},
        )
    ]
