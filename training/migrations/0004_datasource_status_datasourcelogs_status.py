# Generated by Django 4.2.13 on 2024-06-12 06:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0003_remove_datasource_data_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="datasource",
            name="status",
            field=models.CharField(default=django.utils.timezone.now, max_length=155),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datasourcelogs",
            name="status",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
