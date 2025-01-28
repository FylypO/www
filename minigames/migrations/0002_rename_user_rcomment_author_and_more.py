# Generated by Django 4.2 on 2025-01-12 22:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("minigames", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rcomment",
            old_name="user",
            new_name="author",
        ),
        migrations.RenameField(
            model_name="review",
            old_name="user",
            new_name="author",
        ),
        migrations.AddField(
            model_name="rcomment",
            name="dislikes",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="rcomment",
            name="likes",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="post",
            name="dislikes",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="post",
            name="likes",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="review",
            name="dislikes",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="review",
            name="likes",
            field=models.IntegerField(default=0),
        ),
    ]
