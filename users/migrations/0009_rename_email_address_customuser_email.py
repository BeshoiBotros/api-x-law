# Generated by Django 5.0 on 2024-01-29 23:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_rename_email_customuser_email_address"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="email_address",
            new_name="email",
        ),
    ]
