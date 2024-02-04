# Generated by Django 5.0 on 2024-02-04 13:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscribes", "0004_subscribecontract_nums_of_users_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscribecontract",
            name="subscribe_order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="subscribes.subscribeorder",
            ),
        ),
    ]
