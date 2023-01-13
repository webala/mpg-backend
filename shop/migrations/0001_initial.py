# Generated by Django 4.1.5 on 2023-01-12 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=20)),
                ('series', models.CharField(blank=True, max_length=20, null=True)),
                ('model', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=4)),
                ('body_type', models.CharField(max_length=20)),
                ('eingine', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_no', models.CharField(max_length=20)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.car')),
            ],
        ),
    ]
