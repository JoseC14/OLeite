# Generated by Django 5.0.1 on 2024-03-03 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_passrecovery_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passrecovery',
            name='usuario',
        ),
    ]
