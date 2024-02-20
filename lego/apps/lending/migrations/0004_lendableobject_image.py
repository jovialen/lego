# Generated by Django 4.0.10 on 2024-02-20 19:45

from django.db import migrations
import django.db.models.deletion
import lego.apps.files.models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_file_save_for_use'),
        ('lending', '0003_remove_lendableobject_responsible_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lendableobject',
            name='image',
            field=lego.apps.files.models.FileField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lendable_object_images', to='files.file'),
        ),
    ]
