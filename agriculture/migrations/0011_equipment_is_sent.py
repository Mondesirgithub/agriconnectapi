# Generated by Django 4.2.7 on 2023-12-13 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agriculture', '0010_equipment_rental_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='is_sent',
            field=models.BooleanField(default=False),
        ),
    ]