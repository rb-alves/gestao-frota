# Generated by Django 5.0.6 on 2024-06-13 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("colaboradores", "0006_alter_colaborador_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cargo",
            name="descricao",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
