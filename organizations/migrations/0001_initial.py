# Generated by Django 5.0 on 2024-03-16 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('subscribes', '__first__'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('swift_number', models.CharField(blank=True, max_length=255, null=True)),
                ('currency', models.CharField(choices=[('USD', 'United States dollar'), ('EUR', 'the Euro'), ('EGP', 'Egyptian pound')], max_length=10)),
                ('discription', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Big Lawyer', max_length=255, unique=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=16, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subscribe_contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscribes.subscribecontract')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.lawyer')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectOwnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
            ],
        ),
    ]
