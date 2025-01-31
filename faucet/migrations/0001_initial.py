# Generated by Django 5.1.1 on 2024-09-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                ("wallet_address", models.CharField(max_length=255)),
                ("tx_id", models.CharField(blank=True, max_length=255, null=True)),
                ("status", models.CharField(max_length=50)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
