from django.db import models
from fornecedores.models import Fornecedor
from colaboradores.models import Colaborador
from datetime import datetime


class GrupoVeiculo(models.Model):
    descricao = models.CharField(max_length=255, unique=True, null=False, blank=False)

    class Meta:
        db_table = "grupos_veiculos"

    def __str__(self):
        return self.descricao


class Combustivel(models.Model):
    descricao = models.CharField(max_length=255, unique=True, null=False, blank=False)

    class Meta:
        db_table = "combustiveis"

    def __str__(self):
        return self.descricao


class Veiculo(models.Model):
    placa = models.CharField(max_length=7, unique=True)

    porte = models.CharField(
        max_length=100,
        choices=[("Pequeno", "Pequeno"), ("Médio", "Médio"), ("Grande", "Grande")],
        null=False,
        blank=False,
    )

    modelo = models.CharField(max_length=100, null=False, blank=False)
    marca = models.CharField(max_length=100, null=False, blank=False)
    ano = models.IntegerField(null=False, blank=False)
    combustivel = models.ForeignKey(Combustivel, on_delete=models.SET_NULL, null=True)
    renavam = models.CharField(max_length=100, null=False, blank=False)
    chassi = models.CharField(max_length=100, null=False, blank=False)
    grupo_veiculo = models.ForeignKey(
        GrupoVeiculo, on_delete=models.SET_NULL, null=True
    )

    situacao = models.CharField(
        max_length=100,
        choices=[("Ativo", "Ativo"), ("Inativo", "Inativo")],
        default="Ativo",
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "veiculos"

    def __str__(self):
        return self.placa


class Maquina(models.Model):
    identificacao = models.CharField(
        max_length=255, null=False, blank=False, unique=True
    )
    modelo = models.CharField(max_length=255, null=False, blank=False)
    grupo_veiculo = models.ForeignKey(
        GrupoVeiculo, on_delete=models.SET_NULL, null=True
    )
    situacao = models.CharField(
        max_length=100,
        choices=[("Ativo", "Ativo"), ("Inativo", "Inativo")],
        default="Ativo",
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "maquinas"

    def __str__(self):
        return self.identificacao


class Tipo(models.Model):
    descricao = models.CharField(max_length=255, null=False, blank=False, unique=True)

    class Meta:
        db_table = "tipos_manutencoes"

    def __str__(self):
        return self.descricao


class Causa(models.Model):
    descricao = models.CharField(max_length=255, null=False, blank=False, unique=True)

    class Meta:
        db_table = "causas_manutencoes"

    def __str__(self):
        return self.descricao


class CentroCusto(models.Model):
    descricao = models.CharField(max_length=255, null=False, blank=False, unique=True)

    class Meta:
        db_table = "centros_custos"

    def __str__(self):
        return self.descricao


class ManutencaoVeiculo(models.Model):
    data = models.DateField(null=False, blank=False)
    documento = models.CharField(null=False, blank=False, max_length=255)
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True, blank=False
    )
    tipo = models.ForeignKey(Tipo, on_delete=models.SET_NULL, null=True, blank=False)
    causa = models.ForeignKey(Causa, on_delete=models.SET_NULL, null=True, blank=False)
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.SET_NULL, null=True, blank=False
    )
    centro_custo = models.ForeignKey(
        CentroCusto, on_delete=models.SET_NULL, null=True, blank=False
    )
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.SET_NULL, null=True, blank=False
    )
    descricao = models.TextField(null=False, blank=False)
        

    class Meta:
        db_table = "manutencoes_veiculos"

    def __str__(self):
        return f"Manutenção - {self.documento} - Veiculo: {self.veiculo}"



class ManutencaoMaquina(models.Model):
    data = models.DateField(null=False, blank=False)
    documento = models.CharField(null=False, blank=False, max_length=255)
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True, blank=False
    )
    tipo = models.ForeignKey(Tipo, on_delete=models.SET_NULL, null=True, blank=False)
    causa = models.ForeignKey(Causa, on_delete=models.SET_NULL, null=True, blank=False)
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.SET_NULL, null=True, blank=False
    )
    centro_custo = models.ForeignKey(
        CentroCusto, on_delete=models.SET_NULL, null=True, blank=False
    )
    maquina = models.ForeignKey(
        Maquina, on_delete=models.SET_NULL, null=True, blank=False
    )
    descricao = models.TextField(null=False, blank=False)
        

    class Meta:
        db_table = "manutencoes_maquinas"

    def __str__(self):
        return f"Manutenção - {self.documento} - Maquina: {self.maquina}"


class ManutencaoGeral(models.Model):
    data = models.DateField(null=False, blank=False)
    documento = models.CharField(null=False, blank=False, max_length=255)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=False)
    descricao = models.TextField(null=False, blank=False)
    causa = models.ForeignKey(Causa, on_delete=models.SET_NULL, null=True, blank=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    tipo = models.CharField(max_length=100, choices=[("Veículos", "Veículos"), ("Máquinas", "Máquinas"), ("Paleteira", "Paleteira")], null=False, blank=False)
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        db_table = "manutencoes_gerais"

    
    def __str__(self):
        return f"Manutenção Geral: {self.documento} - Valor: {self.valor}"



class Abastecimento(models.Model):
    data = models.DateField(null=False, blank=False)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.SET_NULL, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True)
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.SET_NULL, null=True)
    tipo_combustivel = models.ForeignKey(Combustivel, on_delete=models.SET_NULL, null=True)
    litros = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    hodometro_transacao = models.PositiveIntegerField(null=False, blank=False)
    hodometro_anterior = models.PositiveIntegerField(null=False, blank=False)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    valor_transacao = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    class Meta:
        db_table = "abastecimentos"
    
    def __str__(self):
        return f"Abastecimento em {self.data_hora} - {self.tipo_combustivel} Placa {self.veiculo}"
    
    
    # Calcula o KM percorrido na tabela
    def km_percorrido(self):
        percorrido = self.hodometro_transacao - self.hodometro_anterior
        return percorrido
    
    # Calcula a média de consumo na tabela
    def media_consumo(self):
        if self.litros > 0:
            media = self.km_percorrido() / self.litros
            return f"{media:.2f}"
        return "N/A"