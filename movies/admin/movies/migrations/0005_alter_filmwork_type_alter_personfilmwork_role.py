# Generated by Django 4.2.4 on 2023-09-02 20:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_alter_genrefilmwork_genre"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filmwork",
            name="type",
            field=models.TextField(
                choices=[("movie", "movie"), ("tv_show", "tv_show")],
                verbose_name="type",
            ),
        ),
        migrations.AlterField(
            model_name="personfilmwork",
            name="role",
            field=models.TextField(
                blank=True,
                choices=[
                    ("actor", "actor"),
                    ("director", "director"),
                    ("writer", "writer"),
                ],
                verbose_name="role",
            ),
        ),
    ]