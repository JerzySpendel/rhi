# Generated by Django 4.0.5 on 2022-06-07 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asteroid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('mass', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('mass', models.FloatField(null=True)),
                ('polar_radius', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Moon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mass', models.FloatField()),
                ('planet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sky.planet')),
            ],
        ),
    ]