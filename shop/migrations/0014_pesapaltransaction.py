# Generated by Django 4.1.5 on 2023-02-08 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0013_alter_mpesatransaction_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="PesapalTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_tracking_id", models.CharField(max_length=50)),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shop.order",
                    ),
                ),
            ],
        ),
    ]
