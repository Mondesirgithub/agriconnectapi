# Generated by Django 4.2.7 on 2023-12-10 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agriculture', '0005_alter_equipment_owner_alter_equipment_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='slug',
        ),
    ]
