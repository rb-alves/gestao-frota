from django.db import models


class EspecialidadeFornecedor(models.Model):
    descricao = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        db_table = "especialidades_fornecedores"

    def __str__(self):
        return self.descricao


class Fornecedor(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False, unique=True)
    razao_social = models.CharField(max_length=255, null=True)
    cnpj = models.CharField(max_length=20, null=True)
    telefone = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=100, null=True)
    especialidade = models.ForeignKey(
        EspecialidadeFornecedor, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = "fornecedores"

    def __str__(self):
        return self.nome
