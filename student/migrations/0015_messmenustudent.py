# Generated by Django 4.2.7 on 2023-11-29 18:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0014_delete_messmenustudent"),
    ]

    operations = [
        migrations.CreateModel(
            name="MessMenuStudent",
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
                ("excel_file", models.FileField(upload_to="")),
                ("uploaded_at", models.DateTimeField()),
            ],
        ),
    ]
