# Generated by Django 4.2.7 on 2023-11-27 13:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0003_alter_studentprofile_bits_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentprofile",
            name="email_id",
        ),
        migrations.RemoveField(
            model_name="studentprofile",
            name="mess",
        ),
        migrations.RemoveField(
            model_name="studentprofile",
            name="name",
        ),
        migrations.RemoveField(
            model_name="studentprofile",
            name="profile_image",
        ),
        migrations.RemoveField(
            model_name="studentprofile",
            name="user",
        ),
    ]
