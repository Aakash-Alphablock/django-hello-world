# Generated by Django 4.2.13 on 2024-06-12 05:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0002_datasource_version_alter_datasource_category_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="datasource",
            name="data_type",
        ),
    ]
