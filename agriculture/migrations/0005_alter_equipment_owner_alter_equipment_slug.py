# Generated by Django 4.2.7 on 2023-12-10 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agriculture', '0004_rename_location_equipment_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_equipment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='slug',
            field=models.SlugField(blank=True, max_length=128, null=True),
        ),
    ]
