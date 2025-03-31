from django.shortcuts import render, redirect, get_object_or_404
from frota.models import Veiculo, Combustivel, GrupoVeiculo, Maquina, ManutencaoVeiculo, ManutencaoMaquina, ManutencaoGeral, Tipo, Causa, CentroCusto, Abastecimento
from fornecedores.models import Fornecedor
from colaboradores.models import Colaborador
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


def formataValor(valor):
    """
    Converte um valor monetário no formato brasileiro para um float.
    Retorna None para valores vazios ou inválidos.
    """
    if not valor or valor.strip() == "R$":
        return None  # Retorna None se o valor for vazio ou apenas o prefixo "R$"
    
    try:
        # Remove "R$ ", pontos de milhar e substitui a vírgula decimal por ponto
        valor = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(valor)
    except ValueError:
        # Retorna None se a conversão falhar
        return None




@login_required
def listaVeiculos(request):
    # Busca todos os veiculos ordenados por placa
    veiculos = Veiculo.objects.all().order_by("placa")

    # Inicializa as variáveis do filtro como vazias
    situacao = ""
    placa = ""
    marca = ""
    modelo = ""
    ano = ""
    porte = ""
    combustivel = ""
    grupo_veiculo = ""
    chassi = ""
    renavam = ""

    # Verifica se existe uma requisição tipo POST para aplicar os filtros
    if request.method == "POST":
        # Filtros
        # Obtém o valor do filtro retorna uma string vazia ("") caso não exista
        situacao = request.POST.get("filtro-situacao", "")
        if situacao:
            veiculos = veiculos.filter(situacao=situacao)
        
        placa = request.POST.get("filtro-placa", "")
        if placa:
            veiculos = veiculos.filter(placa__icontains=placa)
        
        marca = request.POST.get("filtro-marca", "")
        if marca:
            veiculos = veiculos.filter(marca__icontains=marca)
        
        modelo = request.POST.get("filtro-modelo", "")
        if modelo:
            veiculos = veiculos.filter(modelo__icontains=modelo)
        
        ano = request.POST.get("filtro-ano", "")
        if ano:
            veiculos = veiculos.filter(ano__icontains=ano)
        
        porte = request.POST.get("filtro-porte", "")
        if porte:
            veiculos = veiculos.filter(porte=porte)
        
        combustivel = request.POST.get("filtro-combustivel", "")
        if combustivel:
            combustivel = int(combustivel)
            veiculos = veiculos.filter(combustivel=combustivel)
        
        grupo_veiculo = request.POST.get("filtro-grupo_veiculo", "")
        if grupo_veiculo:
            grupo_veiculo = int(grupo_veiculo)
            veiculos = veiculos.filter(grupo_veiculo=grupo_veiculo)
        
        chassi = request.POST.get("filtro-chassi", "")
        if chassi:
            veiculos = veiculos.filter(chassi__icontains=chassi)
        
        renavam = request.POST.get("filtro-renavam", "")
        if renavam:
            veiculos = veiculos.filter(renavam__icontains=renavam)
        

    # Dados para template completo
    portes = Veiculo._meta.get_field("porte").choices
    combustiveis = Combustivel.objects.all().order_by("descricao")
    grupos_veiculos = GrupoVeiculo.objects.all().order_by("descricao")
    situacoes = Veiculo._meta.get_field("situacao").choices


    return render(
        request,
        "frota/veiculos/lista_veiculos.html",
        {
            "veiculos": veiculos,
            "portes": portes,
            "combustiveis": combustiveis,
            "grupos_veiculos": grupos_veiculos,
            "situacoes": situacoes,
            "filtro_situacao": situacao,
            "filtro_placa": placa,
            "filtro_marca": marca,
            "filtro_modelo": modelo,
            "filtro_ano": ano,
            "filtro_porte": porte,
            "filtro_combustivel": combustivel,
            "filtro_grupo_veiculo": grupo_veiculo,
            "filtro_chassi": chassi,
            "filtro_renavam": renavam

        },
    )


# Cria um novo veiculo no banco de dados
def novoVeiculo(request):
    # Verifica se a requisição enviada é do tipo POST
    if request.method == "POST":
        # Recupera as informações do formulário
        placa = request.POST.get("placa").upper()
        marca = request.POST.get("marca").capitalize()
        modelo = request.POST.get("modelo").upper()
        ano = request.POST.get("ano")
        porte = request.POST.get("porte")
        combustivel = request.POST.get("combustivel")
        grupo_veiculo = request.POST.get("grupo_veiculo")
        chassi = request.POST.get("chassi")
        renavam = request.POST.get("renavam")

        # Busca os objeto especialidade pelo ID fornecido
        combustivel = Combustivel.objects.get(id=combustivel)
        grupo_veiculo = GrupoVeiculo.objects.get(id=grupo_veiculo)

        # Verifica se o campo placa não está vazio
        if placa != "":
            # tenta cadastrar um novo veículo
            try:
                # Cria um novo registro no banco de dados
                cadastrar_veiculo = Veiculo(
                    placa=placa,
                    porte=porte,
                    modelo=modelo,
                    marca=marca,
                    ano=ano,
                    combustivel=combustivel,
                    chassi=chassi,
                    renavam=renavam,
                    grupo_veiculo=grupo_veiculo,
                )

                # Salva o registro no banco de dados
                cadastrar_veiculo.save()
                messages.success(request, "O veículo foi cadastrado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar o veículo: {str(e)}")

        else:
            messages.error(
                request, "Erro ao cadastrar o veículo: O campo placa está vazio"
            )

        # Retorna a listagem  de veículos em caso de sucesso ou fracasso
        return redirect("lista_veiculos")


def editarVeiculo(request, veiculo_id):
    # A função get_object_or_404 possui dois argumentos (TABELA DO BANCO E ID)
    # Caso a função encontre o ID na tabela o registro é retornado, caso o ID não seja encontrado ocorrera um erro 404
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)

    # Variaveis usadas para passar contexto para o template
    portes = Veiculo._meta.get_field("porte").choices
    situacoes = Veiculo._meta.get_field("situacao").choices
    combustiveis = Combustivel.objects.all().order_by("descricao")
    grupos_veiculos = GrupoVeiculo.objects.all().order_by("descricao")

    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os dados vindos do formulário
        placa = request.POST.get("placa")
        marca = request.POST.get("marca")
        modelo = request.POST.get("modelo")
        ano = request.POST.get("ano")
        porte = request.POST.get("porte")
        combustivel = request.POST.get("combustivel")
        grupo_veiculo = request.POST.get("grupo_veiculo")
        chassi = request.POST.get("chassi")
        renavam = request.POST.get("renavam")
        situacao = request.POST.get("situacao")

        # Busca os objetos Cargos e Departamentos pelos IDs fornecidos
        combustivel = Combustivel.objects.get(id=combustivel)
        grupo_veiculo = GrupoVeiculo.objects.get(id=grupo_veiculo)

        if placa != "":
            # Tenta realizar a edição no banco de dados
            try:
                # edita os dados do registro
                veiculo.placa = placa
                veiculo.marca = marca
                veiculo.modelo = modelo
                veiculo.ano = ano
                veiculo.porte = porte
                veiculo.combustivel = combustivel
                veiculo.grupo_veiculo = grupo_veiculo
                veiculo.chassi = chassi
                veiculo.renavam = renavam
                veiculo.situacao = situacao

                # Salva as mudanças no banco de dados
                veiculo.save()

                # Mensagem de sucesso
                messages.success(request, "O veículo foi atualizado com sucesso!")

            except Exception as e:
                # Mensagem de fracasso
                messages.error(request, f"Erro ao atualizar o veículo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao atualizar o veículo: O campo placa está vazio"
            )

        return redirect("lista_veiculos")

    return render(
        request,
        "frota/veiculos/editar_veiculo.html",
        {
            "veiculo": veiculo,
            "portes": portes,
            "combustiveis": combustiveis,
            "grupos_veiculos": grupos_veiculos,
            "situacoes": situacoes,
        },
    )


# Exclui um veículo do banco de dados
def excluirVeiculo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera o ID enviado pelo modal de exclusão
        veiculo_id = request.POST.get("idVeiculo")

        # Encontra na tabela VEICULO um id = ao enviado caso não encontre erro 404
        veiculo = get_object_or_404(Veiculo, pk=veiculo_id)

        # Tenta realizar a exclusão
        try:
            veiculo.delete()
            messages.success(request, "O veículo foi excluído com sucesso")

        except Exception as e:
            messages.error(request, f"Erro ao excluir veículo: {str(e)}")

        return redirect("lista_veiculos")


########################################## MAQUINAS ###########################################

@login_required
def listaMaquinas(request):
    # Busca todas as máquinas ordenadas por identificação
    maquinas = Maquina.objects.all().order_by("identificacao")

    # Inicializa as variáveis do filtro como vazias
    situacao = ""
    identificacao = ""
    modelo = ""
    grupo_veiculo = ""

    # Verifica se existe uma requisição tipo POST para aplicar os filtros
    if request.method == "POST":
        # Filtros
        situacao = request.POST.get("situacao", "")
        if situacao:
            maquinas = maquinas.filter(situacao=situacao)

        identificacao = request.POST.get("filtro-ident", "")
        if identificacao:
            maquinas = maquinas.filter(identificacao__icontains=identificacao)

        modelo = request.POST.get("filtro-modelo", "")
        if modelo:
            maquinas = maquinas.filter(modelo__icontains=modelo)

        grupo_veiculo = request.POST.get("filtro-grupo_veiculo", "")
        if grupo_veiculo:
            grupo_veiculo = int(grupo_veiculo)
            maquinas = maquinas.filter(grupo_veiculo=grupo_veiculo)

    # Dados adicionais para o template
    grupos = GrupoVeiculo.objects.all().order_by("descricao")
    situacoes = Maquina._meta.get_field("situacao").choices

    return render(
        request,
        "frota/maquinas/lista_maquinas.html",
        {
            "maquinas": maquinas,
            "grupos": grupos,
            "situacoes": situacoes,
            "filtro_situacao": situacao,
            "filtro_identificacao": identificacao,
            "filtro_modelo": modelo,
            "filtro_grupo_veiculo": grupo_veiculo,
        },
    )

def novaMaquina(request):
    # Verifica se a requisição enviada é do tipo POST
    if request.method == "POST":
        # Recupera os dados enviados pelo formulário
        identificacao = request.POST.get("ident").upper()
        modelo = request.POST.get("modelo").upper()
        grupo_veiculo = request.POST.get("grupo_veiculo")

        # Busca os objeto grupo pelo ID fornecido
        grupo_veiculo = GrupoVeiculo.objects.get(id=grupo_veiculo)

        if identificacao != "":
            # tenta realizar o cadastro
            try:
                # Cria o registro no banco de dados
                cadastrar_maquina = Maquina(
                    identificacao=identificacao,
                    modelo=modelo,
                    grupo_veiculo=grupo_veiculo,
                )

                # Salva o registro no banco de dados
                cadastrar_maquina.save()

                # Mensagem de sucesso
                messages.success(request, "Máquina cadastrada com sucesso!")

            except Exception as e:
                # Mensagem de erro
                messages.error(request, f"Erro ao atualizar a máquina: {str(e)}")
        else:
            # Mensagem de erro
            messages.error(
                request, "Erro ao atualizar a máquina: O campo identificação está vazio"
            )

        return redirect("lista_maquinas")


# Edita uma maquina já cadastrada no banco de dados
def editarMaquina(request, maquina_id):
    maquina = get_object_or_404(Maquina, pk=maquina_id)
    grupos = GrupoVeiculo.objects.all().order_by("descricao")
    situacoes = Maquina._meta.get_field("situacao").choices

    # Verifica se é uma requisição do tipo POST
    if request.method == "POST":
        # Recupera os valores dos formulários e armazena em variavel
        identificacao = request.POST.get("ident")
        modelo = request.POST.get("modelo")
        grupo_veiculo = request.POST.get("grupo_veiculo")
        situacao = request.POST.get("situacao")

        # Busca os objeto grupo pelo ID fornecido
        grupo_veiculo = GrupoVeiculo.objects.get(id=grupo_veiculo)

        # tenta realizar a edição
        try:
            # Realiza as alterações no banco
            maquina.identificacao = identificacao
            maquina.modelo = modelo
            maquina.grupo_veiculo = grupo_veiculo
            maquina.situacao = situacao

            # Salva as alterações no banco de dados
            maquina.save()
            messages.success(request, "A máquina foi atualizada com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao atualizar a máquina: {str(e)}")

        return redirect("lista_maquinas")

    return render(
        request,
        "frota/maquinas/editar_maquina.html",
        {"grupos": grupos, "maquina": maquina, "situacoes": situacoes},
    )


# Exclui uma maquina já cadastrada no banco de dados
def excluirMaquina(request):
    # Verifica se é uma requisição do tipo POST
    if request.method == "POST":
        # Recupera o valor do ID enviado pelo formulário de exclusão
        maquina_id = request.POST.get("idMaquina")
        # Busca na tabela de máquinas um ID igual ao enviado ou mostra um erro 404
        maquina = get_object_or_404(Maquina, pk=maquina_id)

        try:
            # exclui da tabela o registro encontrado
            maquina.delete()
            messages.success(request, "Máquina excluída com sucesso")

        except Exception as e:
            messages.error(request, f"Erro ao excluir a máquina: {str(e)}")

        # Retorna para a lista de máquinas
        return redirect("lista_maquinas")
