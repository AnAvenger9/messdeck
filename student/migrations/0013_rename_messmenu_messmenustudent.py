# Generated by Django 4.2.7 on 2023-11-29 17:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0012_messmenu"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="MessMenu",
            new_name="MessMenuStudent",
        ),
    ]
