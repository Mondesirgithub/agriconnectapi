# Generated by Django 4.2.7 on 2023-12-06 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0004_alter_utilisateur_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='culture',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
