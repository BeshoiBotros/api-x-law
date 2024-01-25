# Generated by Django 5.0 on 2024-01-24 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("subscribes", "0002_alter_subscribeorder_companyuser"),
        ("users", "0004_lawyerprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
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
                ("name", models.CharField(default="Big Lawyer", max_length=255)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
                ("url", models.URLField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "subscribe_contract",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subscribes.subscribecontract",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.lawyer"
                    ),
                ),
            ],
        ),
    ]