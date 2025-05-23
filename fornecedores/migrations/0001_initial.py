# Generated by Django 5.0.6 on 2024-06-11 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EspecialidadeFornecedor",
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
            options={
                "db_table": "especialidades_fornecedores",
            },
        ),
        migrations.CreateModel(
            name="Fornecedor",
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
                ("nome", models.CharField(max_length=255, unique=True)),
                ("razao_social", models.CharField(max_length=255, null=True)),
                ("cnpj", models.CharField(max_length=20, null=True)),
                ("telefone", models.CharField(max_length=20, null=True)),
                ("email", models.EmailField(max_length=100, null=True)),
                (
                    "especialidade",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="fornecedores.especialidadefornecedor",
                    ),
                ),
            ],
            options={
                "db_table": "fornecedores",
            },
        ),
    ]
