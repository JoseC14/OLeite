# Generated by Django 5.0.1 on 2024-01-22 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chuva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('milimetros', models.IntegerField()),
                ('data', models.DateField(unique=True)),
            ],
        ),
    ]