# Generated by Django 4.1.5 on 2023-01-30 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0011_mpesatransaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mpesatransaction",
            name="phone_number",
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="mpesatransaction",
            name="receipt_number",
            field=models.CharField(max_length=15, null=True),
        ),
    ]
