# Generated by Django 5.0.1 on 2024-01-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chuva', '0002_chuva_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chuva',
            name='data',
            field=models.DateField(),
        ),
    ]