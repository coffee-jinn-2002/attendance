# Generated by Django 5.0.3 on 2024-03-07 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "attendance_app",
            "0002_user_groups_user_is_superuser_user_last_login_and_more",
        ),
    ]

    operations = [
        migrations.DeleteModel(
            name="Organization",
        ),
    ]