# Generated by Django 5.0.4 on 2024-06-11 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0006_rename_description_person_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='address',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='phone',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='job',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
    ]
