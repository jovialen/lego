# Generated by Django 2.0.2 on 2018-02-23 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0015_auto_20180216_2026")]

    operations = [
        migrations.AddField(
            model_name="abakusgroup",
            name="contact_email",
            field=models.EmailField(blank=True, max_length=254),
        )
    ]
