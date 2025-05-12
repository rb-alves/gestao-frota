from django.db import models
from frota.models import Veiculo
from colaboradores.models import Colaborador
from frota.models import CentroCusto
import os
import uuid


class Multa(models.Model):
    data_cadastro = models.DateField(auto_now_add=True)
    data_infracao = models.DateField(null=False, blank=False)
    hora_infracao = models.TimeField(null=False, blank=False)
    auto_infracao = models.CharField(max_length=255, null=False, blank=False, unique=True)

    gravidade = models.CharField(
                                max_length=100, 
                                choices=[("Leve", "Leve"), ("Média", "Média"), ("Grave", "Grave"), ("Gravíssima", "Gravíssima")],
                                null=False,
                                blank=False
                                )
    
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.SET_NULL, null=True)
    data_vencimento = models.DateField(null=False, blank=False)
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.SET_NULL, null=True)

    situacao_multa = models.CharField(max_length=100, 
                                      choices=[("A Pagar", "A Pagar"), ("Pago", "Pago"), ("Recorrendo", "Recorrendo"), ("Anulada", "Anulada")],
                                      default="A Pagar",
                                      null=False,
                                      blank=False
                                      )

    descricao = models.TextField(null=False, blank=False)

    class Meta:
        db_table = "multas"

    def __str__(self):
        return f"Multa: {self.auto_infracao} do veículo {self.veiculo}"
    


# Função que nomeia unicamente os arquivos
def arquivo_unico(intancia, nomeArquivo, pasta):
    extensao = nomeArquivo.split('.')[-1] # Extrai a extensão do arquivo
    nomeArquivo = f'{uuid.uuid4()}.{extensao}' # Gera um nome de arquivo único usando UUID
    return os.path.join(pasta, nomeArquivo) # Retorna o caminho completo para onde o arquivo será salvo
    
# Funções para passar o caminho para cada upload
def caminho_documento_prejudicado(instancia, nomeArquivo):
    return arquivo_unico(instancia, nomeArquivo, 'ocorridos/documentos/')

def caminho_comprovante_pagamento(instancia, nomeArquivo):
    return arquivo_unico(instancia, nomeArquivo, 'ocorridos/comprovantes/')

def caminho_ordem_pagamento(instancia, nomeArquivo):
    return arquivo_unico(instancia, nomeArquivo, 'ocorridos/ordem_pagamento/')

def caminho_orcamento(instancia, nomeArquivo):
    return arquivo_unico(instancia, nomeArquivo, 'ocorridos/orcamento/')

def caminho_foto_ocorrido(instancia, nomeArquivo):
    return arquivo_unico(instancia, nomeArquivo, 'ocorridos/fotos_ocorridos/')

def caminho_video_ocorrido(instancia, nomeArquivo):
    return arquivo_unico(instancia, nomeArquivo, 'ocorridos/videos_ocorrido/')





class Ocorrido(models.Model):
    # Cria a lista de Ocorridos
    TIPO = [
        ("Acidente", "Acidente"),
        ("Incidente", "Incidente"),
        ("Perda ou Furto", "Perda ou Furto")
    ]

    # Cria a lista de situações
    SITUACOES = [
        ("Não Solucionado", "Não Solucionado"),
        ("Solucionado", "Solucionado")
    ]

    # Cria lista de escolhas
    ESCOLHAS = [
        ("Sim", "Sim"),
        ("Não", "Não")
    ]



    #Campos obrigatórios
    data_ocorrido = models.DateField(null=False, blank=False)
    tipo_ocorrido = models.CharField(max_length=100, choices=TIPO, null=False, blank=False)
    descricao = models.TextField(null=False, blank=False)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.SET_NULL, null=True, blank=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True)
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.SET_NULL, null=True, blank=True)
    situacao = models.CharField(max_length=100, choices=SITUACOES, default="Não Solucionado")
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    responsabiliza_condutor = models.CharField(max_length=100, choices=ESCOLHAS, null=False, blank=False)

    #Campos opcionais de indeficação do prejudicado
    prejudicado_nome = models.CharField(max_length=255, null=True, blank=True)
    prejudicado_cpf_cnpj = models.CharField(max_length=20, null=True, blank=True)

    documento_prejudicado = models.FileField(upload_to=caminho_documento_prejudicado, null=True, blank=True)
    comprovante_pagamento = models.FileField(upload_to=caminho_comprovante_pagamento, null=True, blank=True)
    ordem_pagamento = models.FileField(upload_to=caminho_ordem_pagamento, null=True, blank=True)
    orcamento = models.FileField(upload_to=caminho_orcamento, null=True, blank=True)
    
    #Campos de fotos
    foto1 = models.ImageField(upload_to=caminho_foto_ocorrido, null=True, blank=True)
    foto2 = models.ImageField(upload_to=caminho_foto_ocorrido, null=True, blank=True)
    foto3 = models.ImageField(upload_to=caminho_foto_ocorrido, null=True, blank=True)
    foto4 = models.ImageField(upload_to=caminho_foto_ocorrido, null=True, blank=True)
    foto5 = models.ImageField(upload_to=caminho_foto_ocorrido, null=True, blank=True)

    #Campo de video
    video_ocorrido = models.FileField(upload_to=caminho_video_ocorrido, null=True, blank=True)

    class Meta:
        db_table = 'ocorridos'
    
    def __str__(self):
        return f"Ocorrido: {self.tipo_ocorrido}, Data: {self.data_ocorrido}, Colaborador: {self.colaborador}, Veículo: {self.veiculo}"

    



