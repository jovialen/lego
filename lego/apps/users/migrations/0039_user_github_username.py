# Generated by Django 4.0.9 on 2023-05-13 14:05

import django.core.validators
from django.db import migrations, models

import lego.utils.validators


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0038_alter_abakusgroup_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="github_username",
            field=models.CharField(
                help_text="Enter a valid username.",
                max_length=39,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-z\\d](?:[a-z\\d]|-(?=[a-z\\d])){0,38}$",
                        "Enter a valid username. ",
                        "characters.",
                        "invalid",
                    ),
                    lego.utils.validators.ReservedNameValidator(),
                ],
            ),
        ),
    ]
