# Generated by Django 4.2.7 on 2023-12-04 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0002_utilisateur_adresse_utilisateur_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='comptes/utilisateurs'),
        ),
    ]
