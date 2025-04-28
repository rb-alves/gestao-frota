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


########################################## MANUTENÇÕES VEICULOS ####################################

def listaManutencoes(request):
    manutencoes = ManutencaoVeiculo.objects.all().order_by('-id')

    # Inicializa as variáveis do filtro como vazias
    data_inicial = ""
    data_final = ""
    documento = ""
    fornecedor = ""
    centro_custo = ""
    tipo = ""
    causa = ""
    valor = ""
    descricao = ""
    colaborador = ""
    veiculo = ""

    # Verifica se existe uma requisição tipo POST para aplicar os filtros
    if request.method == "POST":
        data_inicial = request.POST.get("filtro-data_inicial", "")
        if data_inicial:
            manutencoes = manutencoes.filter(data__gte=data_inicial)

        data_final = request.POST.get("filtro-data_final", "")
        if data_final:
            manutencoes = manutencoes.filter(data__lte=data_final)

        documento = request.POST.get("filtro-documento", "")
        if documento:
            manutencoes = manutencoes.filter(documento__icontains=documento)

        fornecedor = request.POST.get("filtro-fornecedor", "")
        if fornecedor:
            fornecedor = int(fornecedor)
            manutencoes = manutencoes.filter(fornecedor=fornecedor)

        centro_custo = request.POST.get("filtro-centro_custo", "")
        if centro_custo:
            centro_custo = int(centro_custo)
            manutencoes = manutencoes.filter(centro_custo=centro_custo)

        tipo = request.POST.get("filtro-tipo", "")
        if tipo:
            tipo = int(tipo)
            manutencoes = manutencoes.filter(tipo=tipo)

        causa = request.POST.get("filtro-causa", "")
        if causa:
            causa = int(causa)
            manutencoes = manutencoes.filter(causa_id=causa)

        valor = request.POST.get("filtro-valorManutVeiculo", "")
        valor = formataValor(valor)  # Converte o valor monetário
        if valor is not None:  # Apenas filtra se o valor for válido
            manutencoes = manutencoes.filter(valor=valor)

        descricao = request.POST.get("filtro-descricao", "")
        if descricao:
            manutencoes = manutencoes.filter(descricao__icontains=descricao)

        colaborador = request.POST.get("filtro-motorista", "")
        if colaborador:
            colaborador = int(colaborador)
            manutencoes = manutencoes.filter(colaborador=colaborador)

        veiculo = request.POST.get("filtro-veiculoManutCad", "")
        if veiculo:
            veiculo = int(veiculo)
            manutencoes = manutencoes.filter(veiculo=veiculo)

    # Tipos de Manutenções
    tipo_corretiva = Tipo.objects.get(descricao='Corretiva')
    tipo_preventiva = Tipo.objects.get(descricao='Preventiva')       
    
    # Calcula os valores para os cards
    valor_total = manutencoes.aggregate(total=Sum('valor'))['total'] or 0
    valor_corretiva = manutencoes.filter(tipo=tipo_corretiva).aggregate(total=Sum('valor'))['total'] or 0
    valor_preventiva = manutencoes.filter(tipo=tipo_preventiva).aggregate(total=Sum('valor'))['total'] or 0
    valor_outros = manutencoes.exclude(tipo__in=[tipo_corretiva, tipo_preventiva]).aggregate(total=Sum('valor'))['total'] or 0

    colaboradores = Colaborador.objects.all().filter(situacao="Ativo").filter(
        Q(cargo__descricao="Motorista") |
        Q(cargo__descricao="Técnico de Montagem") |
        Q(cargo__descricao="Externo")
        )
    fornecedores = Fornecedor.objects.all().order_by('nome')
    tipos = Tipo.objects.all().order_by('descricao')
    causas = Causa.objects.all().order_by('descricao')
    centros = CentroCusto.objects.all().order_by('descricao')
    veiculos = Veiculo.objects.all().filter(situacao="Ativo")

    return render(
        request,
        "frota/manutencao_veiculo/manutencoes_veiculos.html",
        {
            "manutencoes": manutencoes,
            "colaboradores": colaboradores,
            "fornecedores": fornecedores,
            "tipos": tipos,
            "centros": centros,
            "causas": causas,
            "veiculos": veiculos,
            "filtro_data_inicial": data_inicial,
            "filtro_data_final": data_final,
            "filtro_documento": documento,
            "filtro_fornecedor": fornecedor,
            "filtro_centro_custo": centro_custo,
            "filtro_tipo": tipo,
            "filtro_causa": causa,
            "filtro_valor": valor,
            "filtro_descricao": descricao,
            "filtro_colaborador": colaborador,
            "filtro_veiculo": veiculo,
            "valor_total": valor_total,
            "valor_corretiva": valor_corretiva,
            "valor_preventiva": valor_preventiva,
            "valor_outros": valor_outros,
        },
    )


# Cadastra uma nova manutenção
def novaManutVeiculo(request):
    # Verifica o metodo de envio dos dados
    if request.method == "POST":
        # Recupera os valores do formulário
        data = request.POST.get('data')
        documento = request.POST.get('documento')
        fornecedor = request.POST.get('fornecedor')
        centro_custo = request.POST.get('centro_custo')
        tipo = request.POST.get('tipo')
        causa = request.POST.get('causa')        
        descricao = request.POST.get('descricao')
        colaborador = request.POST.get('motorista') 
        veiculo = request.POST.get('veiculoManutCad')

        valor = formataValor(request.POST.get('valorManutVeiculo'))



        # Busca os objetos nas tabelas pelos IDs enviados pelo formulário
        fornecedor = Fornecedor.objects.get(id=fornecedor)
        centro_custo = CentroCusto.objects.get(id=centro_custo)
        tipo = Tipo.objects.get(id=tipo)
        causa = Causa.objects.get(id=causa)
        colaborador = Colaborador.objects.get(id=colaborador)
        veiculo = Veiculo.objects.get(id=veiculo)

        try:
            cadastrar_manutencao = ManutencaoVeiculo(
                data=data,
                documento=documento,
                fornecedor=fornecedor,
                centro_custo=centro_custo,
                tipo=tipo,
                causa=causa,
                valor=valor,
                colaborador=colaborador,
                veiculo=veiculo,
                descricao=descricao
            )

            cadastrar_manutencao.save()
            messages.success(request, "Manutenção cadastrada com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar a manutenção: {str(e)}")


        return redirect("lista_manutencoes_veiculos")
    
# Edita uma manutenção no banco de dados
def editarManutVeiculo(request, manutencao_id):
    # Carrega os valores para os inputs de edição
    manutencao = get_object_or_404(ManutencaoVeiculo, pk=manutencao_id)
    colaboradores = Colaborador.objects.all().filter(situacao="Ativo").filter(
    Q(cargo__descricao="Motorista") |
    Q(cargo__descricao="Técnico de Montagem") |
    Q(cargo__descricao="Externo")
    )
    fornecedores = Fornecedor.objects.all().order_by('nome')
    tipos = Tipo.objects.all().order_by('descricao')
    causas = Causa.objects.all().order_by('descricao')
    centros = CentroCusto.objects.all().order_by('descricao')
    veiculos = Veiculo.objects.all().filter(situacao="Ativo")

    # Verifica se o metodo é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário de edição
        data = request.POST.get('data')
        documento = request.POST.get('documento')
        fornecedor = request.POST.get('fornecedor')
        centro_custo = request.POST.get('centro_custo')
        tipo = request.POST.get('tipo')
        causa = request.POST.get('causa')
        descricao = request.POST.get('descricao')
        colaborador = request.POST.get('motorista') 
        veiculo = request.POST.get('veiculo')

        valor = formataValor(request.POST.get('valorManutVeiculo'))
        

        # Busca os objetos nas tabelas pelos IDs enviados pelo formulário
        fornecedor = Fornecedor.objects.get(id=fornecedor)
        centro_custo = CentroCusto.objects.get(id=centro_custo)
        tipo = Tipo.objects.get(id=tipo)
        causa = Causa.objects.get(id=causa)
        colaborador = Colaborador.objects.get(id=colaborador)
        veiculo = Veiculo.objects.get(id=veiculo)

        try:
            manutencao.data = data
            manutencao.documento = documento
            manutencao.fornecedor = fornecedor
            manutencao.centro_custo = centro_custo
            manutencao.tipo = tipo
            manutencao.causa = causa
            manutencao.descricao = descricao
            manutencao.colaborador = colaborador
            manutencao.veiculo = veiculo
            manutencao.valor = valor

            manutencao.save()
            messages.success(request, "A manutenção atualizada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao atualizar a manutenção: {str(e)}")

        return redirect("lista_manutencoes_veiculos")

    return render(
        request, 
        "frota/manutencao_veiculo/editar_manut_veiculos.html", {"manutencao": manutencao, "colaboradores": colaboradores, "fornecedores": fornecedores, "tipos": tipos, "centros": centros, "causas": causas, "veiculos": veiculos})


# Exclui uma manutenção
def excluiManutVeiculo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera o id enviado pelo formulário
        manutencao_id = request.POST.get('idManutencao')
        # Busca na tabela de manutenções um ID igual ao ID enviado pelo modal
        manutencao = get_object_or_404(ManutencaoVeiculo, pk=manutencao_id)

        # Tenta apagar a manutenção 
        try:
            manutencao.delete()
            messages.success(request, "Manutenção excluída com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao excluir a manutenção: {str(e)}")
        
        # Redireciona para a lista de manutenções
        return redirect("lista_manutencoes_veiculos")


########################################## MANUTENÇÕES MAQUINAS ####################################
@login_required
def listaManutencoesMaquinas(request):
    manutencoes = ManutencaoMaquina.objects.all().order_by("-id")
    
    # Inicializa as variáveis do filtro como vazias
    data_inicial = ""
    data_final = ""
    documento = ""
    fornecedor = ""
    centro_custo = ""
    tipo = ""
    causa = ""
    valor = ""
    descricao = ""
    colaborador = ""
    maquina = ""

    # Verifica se existe uma requisição tipo POST para aplicar os filtros
    if request.method == "POST":
        data_inicial = request.POST.get("filtro-data_inicial", "")
        if data_inicial:
            manutencoes = manutencoes.filter(data__gte=data_inicial)

        data_final = request.POST.get("filtro-data_final", "")
        if data_final:
            manutencoes = manutencoes.filter(data__lte=data_final)

        documento = request.POST.get("filtro-documento", "")
        if documento:
            manutencoes = manutencoes.filter(documento__icontains=documento)

        fornecedor = request.POST.get("filtro-fornecedor", "")
        if fornecedor:
            fornecedor = int(fornecedor)
            manutencoes = manutencoes.filter(fornecedor=fornecedor)

        centro_custo = request.POST.get("filtro-centro_custo", "")
        if centro_custo:
            centro_custo = int(centro_custo)
            manutencoes = manutencoes.filter(centro_custo=centro_custo)

        tipo = request.POST.get("filtro-tipo", "")
        if tipo:
            tipo = int(tipo)
            manutencoes = manutencoes.filter(tipo=tipo)

        causa = request.POST.get("filtro-causa", "")
        if causa:
            causa = int(causa)
            manutencoes = manutencoes.filter(causa_id=causa)

        valor = request.POST.get("filtro-valorManutMaquina", "")
        valor = formataValor(valor)  # Converte o valor monetário
        if valor is not None:  # Apenas filtra se o valor for válido
            manutencoes = manutencoes.filter(valor=valor)

        descricao = request.POST.get("filtro-descricao", "")
        if descricao:
            manutencoes = manutencoes.filter(descricao__icontains=descricao)

        colaborador = request.POST.get("filtro-maquinista", "")
        if colaborador:
            colaborador = int(colaborador)
            manutencoes = manutencoes.filter(colaborador=colaborador)

        maquina = request.POST.get("filtro-maquinaManutCad", "")
        if maquina:
            maquina = int(maquina)
            manutencoes = manutencoes.filter(maquina=maquina)
    
    # Tipos de Manutenções
    tipo_corretiva = Tipo.objects.get(descricao='Corretiva')
    tipo_preventiva = Tipo.objects.get(descricao='Preventiva')       

    # Calcula os valores para os cards
    valor_total = manutencoes.aggregate(total=Sum('valor'))['total'] or 0
    valor_corretiva = manutencoes.filter(tipo=tipo_corretiva).aggregate(total=Sum('valor'))['total'] or 0
    valor_preventiva = manutencoes.filter(tipo=tipo_preventiva).aggregate(total=Sum('valor'))['total'] or 0
    valor_outros = manutencoes.exclude(tipo__in=[tipo_corretiva, tipo_preventiva]).aggregate(total=Sum('valor'))['total'] or 0

   
    
    # Passa o resto dos contextos para o template
    colaboradores = Colaborador.objects.all().filter(situacao="Ativo").filter(Q(cargo__descricao="Operador de empilhadeira") | Q(cargo__descricao="Operador de transpaleteira"))
    fornecedores = Fornecedor.objects.all().order_by('nome')
    tipos = Tipo.objects.all().order_by('descricao')
    causas = Causa.objects.all().order_by('descricao')
    centros = CentroCusto.objects.all().order_by('descricao')
    maquinas = Maquina.objects.all().filter(situacao="Ativo")

    return render(request, "frota/manutencao_maquina/manutencoes_maquinas.html", {
        "manutencoes": manutencoes, 
        "colaboradores": colaboradores, 
        "fornecedores": fornecedores, 
        "tipos": tipos, 
        "centros": centros, 
        "causas": causas, 
        "maquinas": maquinas,
        "filtro_data_inicial": data_inicial,
        "filtro_data_final": data_final,
        "filtro_documento": documento,
        "filtro_fornecedor": fornecedor,
        "filtro_centro_custo": centro_custo,
        "filtro_tipo": tipo,
        "filtro_causa": causa,
        "filtro_valor": valor,
        "filtro_descricao": descricao,
        "filtro_colaborador": colaborador,
        "filtro_maquina": maquina,
        "valor_total": valor_total,
        "valor_corretiva": valor_corretiva,
        "valor_preventiva": valor_preventiva,
        "valor_outros": valor_outros,

        })



# Cadastra uma nova manutenção
def novaManutMaquina(request):
    # Verifica o metodo de envio dos dados
    if request.method == "POST":
        # Recupera os valores do formulário
        data = request.POST.get('data')
        documento = request.POST.get('documento')
        fornecedor = request.POST.get('fornecedor')
        centro_custo = request.POST.get('centro_custo')
        tipo = request.POST.get('tipo')
        causa = request.POST.get('causa')        
        descricao = request.POST.get('descricao')
        colaborador = request.POST.get('maquinista') 
        maquina = request.POST.get('maquinaManutCad')

        valor = formataValor(request.POST.get('valorManutMaquina'))



        # Busca os objetos nas tabelas pelos IDs enviados pelo formulário
        fornecedor = Fornecedor.objects.get(id=fornecedor)
        centro_custo = CentroCusto.objects.get(id=centro_custo)
        tipo = Tipo.objects.get(id=tipo)
        causa = Causa.objects.get(id=causa)
        colaborador = Colaborador.objects.get(id=colaborador)
        maquina = Maquina.objects.get(id=maquina)

        try:
            cadastrar_manutencao = ManutencaoMaquina(
                data=data,
                documento=documento,
                fornecedor=fornecedor,
                centro_custo=centro_custo,
                tipo=tipo,
                causa=causa,
                valor=valor,
                colaborador=colaborador,
                maquina=maquina,
                descricao=descricao
            )

            cadastrar_manutencao.save()
            messages.success(request, "Manutenção cadastrada com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar a manutenção: {str(e)}")


        return redirect("lista_manutencoes_maquinas")


# Edita uma manutenção no banco de dados
def editarManutMaquina(request, manutencao_id):
    # Carrega os valores para os inputs de edição
    manutencao = get_object_or_404(ManutencaoMaquina, pk=manutencao_id)
    colaboradores = Colaborador.objects.all().filter(situacao="Ativo").filter(Q(cargo__descricao="Operador de empilhadeira") | Q(cargo__descricao="Operador de transpaleteira"))
    fornecedores = Fornecedor.objects.all().order_by('nome')
    tipos = Tipo.objects.all().order_by('descricao')
    causas = Causa.objects.all().order_by('descricao')
    centros = CentroCusto.objects.all().order_by('descricao')
    maquinas = Maquina.objects.all().filter(situacao="Ativo")

    

    # Verifica se o metodo é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário de edição
        data = request.POST.get('data')
        documento = request.POST.get('documento')
        fornecedor = request.POST.get('fornecedor')
        centro_custo = request.POST.get('centro_custo')
        tipo = request.POST.get('tipo')
        causa = request.POST.get('causa')
        descricao = request.POST.get('descricao')
        colaborador = request.POST.get('maquinista') 
        maquina = request.POST.get('maquinaManutEdit')

        valor = formataValor(request.POST.get('valorManutMaquina'))
        

        # Busca os objetos nas tabelas pelos IDs enviados pelo formulário
        fornecedor = Fornecedor.objects.get(id=fornecedor)
        centro_custo = CentroCusto.objects.get(id=centro_custo)
        tipo = Tipo.objects.get(id=tipo)
        causa = Causa.objects.get(id=causa)
        colaborador = Colaborador.objects.get(id=colaborador)
        maquina = Maquina.objects.get(id=maquina)

        try:
            manutencao.data = data
            manutencao.documento = documento
            manutencao.fornecedor = fornecedor
            manutencao.centro_custo = centro_custo
            manutencao.tipo = tipo
            manutencao.causa = causa
            manutencao.descricao = descricao
            manutencao.colaborador = colaborador
            manutencao.maquina = maquina
            manutencao.valor = valor

            manutencao.save()
            messages.success(request, "A manutenção atualizada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao atualizar a manutenção: {str(e)}")

        return redirect("lista_manutencoes_maquinas")

    return render(request, "frota/manutencao_maquina/editar_manut_maquinas.html", {"manutencao": manutencao, "colaboradores": colaboradores, "fornecedores": fornecedores, "tipos": tipos, "centros": centros, "causas": causas, "maquinas": maquinas})

# Exclui uma manutenção
def excluiManutMaquina(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera o id enviado pelo formulário
        manutencao_id = request.POST.get('idManutencao')
        # Busca na tabela de manutenções um ID igual ao ID enviado pelo modal
        manutencao = get_object_or_404(ManutencaoMaquina, pk=manutencao_id)

        # Tenta apagar a manutenção 
        try:
            manutencao.delete()
            messages.success(request, "Manutenção excluída com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao excluir a manutenção: {str(e)}")
        
        # Redireciona para a lista de manutenções
        return redirect("lista_manutencoes_maquinas")
    
