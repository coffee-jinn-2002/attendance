# Generated by Django 5.0.3 on 2024-03-10 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "attendance_app",
            "0009_remove_attendance_user_remove_break_attendance_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="workday",
            name="report",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
