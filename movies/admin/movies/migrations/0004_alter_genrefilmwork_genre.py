# Generated by Django 4.2.4 on 2023-09-02 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0003_make_film_work_person_role_idx"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genrefilmwork",
            name="genre",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="movies.genre",
                verbose_name="genre",
            ),
        ),
    ]
