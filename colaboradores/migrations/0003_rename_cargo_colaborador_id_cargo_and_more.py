# Generated by Django 5.0.6 on 2024-05-28 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("colaboradores", "0002_rename_id_cargo_colaborador_cargo_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="colaborador",
            old_name="cargo",
            new_name="id_cargo",
        ),
        migrations.RenameField(
            model_name="colaborador",
            old_name="departamento",
            new_name="id_departamento",
        ),
    ]
