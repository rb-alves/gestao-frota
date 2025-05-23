# Generated by Django 5.0.6 on 2024-05-28 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cargo",
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
                ("descricao", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Departamento",
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
                ("descricao", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Colaborador",
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
                ("matricula", models.IntegerField(unique=True)),
                ("nome", models.CharField(max_length=255)),
                (
                    "situacao",
                    models.CharField(
                        choices=[
                            ("Ativo", "Ativo"),
                            ("Afastado", "Afastado"),
                            ("Demitido", "Demitido"),
                        ],
                        default="Atico",
                        max_length=100,
                    ),
                ),
                ("admissao", models.DateField()),
                ("desligamento", models.DateField(null=True)),
                (
                    "id_cargo",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="colaboradores.cargo",
                    ),
                ),
                (
                    "id_departamento",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="colaboradores.departamento",
                    ),
                ),
            ],
        ),
    ]
