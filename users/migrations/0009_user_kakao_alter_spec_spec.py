# Generated by Django 4.2.7 on 2023-11-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_user_age_user_android_user_backend_user_frontend_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="kakao",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="spec",
            name="spec",
            field=models.TextField(null=True),
        ),
    ]
