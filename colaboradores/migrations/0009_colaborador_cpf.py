# Generated by Django 5.0.6 on 2024-11-25 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("colaboradores", "0008_alter_departamento_descricao"),
    ]

    operations = [
        migrations.AddField(
            model_name="colaborador",
            name="cpf",
            field=models.CharField(blank=True, default="123", max_length=20, null=True),
        ),
    ]
