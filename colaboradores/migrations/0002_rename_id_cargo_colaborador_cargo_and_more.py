# Generated by Django 5.0.6 on 2024-05-28 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("colaboradores", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="colaborador",
            old_name="id_cargo",
            new_name="cargo",
        ),
        migrations.RenameField(
            model_name="colaborador",
            old_name="id_departamento",
            new_name="departamento",
        ),
    ]
