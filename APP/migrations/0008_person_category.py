# Generated by Django 5.0.6 on 2024-06-15 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0007_rename_address_person_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='category',
            field=models.CharField(choices=[('VEG', 'Vegetables'), ('ICE', 'Ice creams'), ('FRU', 'Fruits'), ('GRO', 'Groceries')], default='VEG', max_length=3),
        ),
    ]