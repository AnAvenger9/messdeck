# Generated by Django 4.2.7 on 2023-11-29 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("staff", "0002_messmenu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="messmenu",
            name="uploaded_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]