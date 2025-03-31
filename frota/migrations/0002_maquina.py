# Generated by Django 5.0.6 on 2024-06-18 18:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("frota", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Maquina",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("identificacao", models.CharField(max_length=255, unique=True)),
                ("modelo", models.CharField(max_length=255)),
                (
                    "grupo_veiculo",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="frota.grupoveiculo",
                    ),
                ),
            ],
            options={
                "db_table": "maquinas",
            },
        ),
    ]
