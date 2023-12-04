# Generated by Django 4.2.7 on 2023-11-27 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentprofile",
            name="bits_id",
            field=models.CharField(
                default=None, max_length=13, null=True
            ),
        ),
        migrations.AddField(
            model_name="studentprofile",
            name="email_id",
            field=models.EmailField(
                default=None, max_length=254, null=True
            ),
        ),
        migrations.AddField(
            model_name="studentprofile",
            name="hostel",
            field=models.CharField(
                default=None, max_length=50, null=True
            ),
        ),
        migrations.AddField(
            model_name="studentprofile",
            name="mess",
            field=models.CharField(
                default=None, max_length=100, null=True
            ),
        ),
        migrations.AddField(
            model_name="studentprofile",
            name="name",
            field=models.CharField(
                default=None, max_length=200, null=True
            ),
        ),
        migrations.AddField(
            model_name="studentprofile",
            name="profile_image",
            field=models.ImageField(default="default.jpg", upload_to="profile_pics"),
        ),
        migrations.AddField(
            model_name="studentprofile",
            name="user",
            field=models.CharField(
                default=None, max_length=200, null=True
            ),
        ),
    ]