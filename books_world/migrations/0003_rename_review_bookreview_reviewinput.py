# Generated by Django 4.2.1 on 2023-06-30 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books_world", "0002_alter_favoritebooks_unique_together_bookreview"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bookreview",
            old_name="review",
            new_name="reviewInput",
        ),
    ]
