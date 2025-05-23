# Generated by Django 5.0.6 on 2024-11-06 20:08

import seguranca.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seguranca", "0010_ocorrido_valor"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ocorrido",
            name="data_finalizacao",
        ),
        migrations.AddField(
            model_name="ocorrido",
            name="responsabiliza_condutor",
            field=models.CharField(
                choices=[(1, "Sim"), (2, "Não")], max_length=100, null=True
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="comprovante_pagamento",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=seguranca.models.caminho_comprovante_pagamento,
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="documento_prejudicado",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=seguranca.models.caminho_documento_prejudicado,
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="foto1",
            field=models.ImageField(
                blank=True, null=True, upload_to=seguranca.models.caminho_foto_ocorrido
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="foto2",
            field=models.ImageField(
                blank=True, null=True, upload_to=seguranca.models.caminho_foto_ocorrido
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="foto3",
            field=models.ImageField(
                blank=True, null=True, upload_to=seguranca.models.caminho_foto_ocorrido
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="foto4",
            field=models.ImageField(
                blank=True, null=True, upload_to=seguranca.models.caminho_foto_ocorrido
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="foto5",
            field=models.ImageField(
                blank=True, null=True, upload_to=seguranca.models.caminho_foto_ocorrido
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="ordem_pagamento",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=seguranca.models.caminho_ordem_pagamento,
            ),
        ),
        migrations.AlterField(
            model_name="ocorrido",
            name="video_ocorrido",
            field=models.FileField(
                blank=True, null=True, upload_to=seguranca.models.caminho_video_ocorrido
            ),
        ),
    ]
