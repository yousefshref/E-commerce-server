# Generated by Django 4.2.7 on 2023-11-24 00:41

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None),
        ),
    ]
