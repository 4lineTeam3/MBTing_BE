# Generated by Django 4.2.7 on 2023-11-08 11:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_user_is_staff"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_staff",
        ),
    ]