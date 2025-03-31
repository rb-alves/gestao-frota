from django.db import models


class Cargo(models.Model):
    descricao = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "cargos"

    def __str__(self):
        return self.descricao


class Departamento(models.Model):
    descricao = models.CharField(max_length=255, null=False, blank=False, unique=True)

    class Meta:
        db_table = "departamentos"

    def __str__(self):
        return self.descricao


class Colaborador(models.Model):
    matricula = models.IntegerField(null=False, blank=False, unique=True)
    nome = models.CharField(max_length=255, null=False, blank=False)
    cpf = models.CharField(max_length=20, null=False, blank=False, unique=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey(
        Departamento, on_delete=models.SET_NULL, null=True
    )
    situacao = models.CharField(
        max_length=100,
        choices=[
            ("Ativo", "Ativo"),
            ("Afastado", "Afastado"),
            ("Demitido", "Demitido"),
        ],
        default="Ativo",
        null=False,
        blank=False,
    )
    admissao = models.DateField(null=False, blank=False)
    desligamento = models.DateField(null=True)

    class Meta:
        db_table = "colaboradores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
