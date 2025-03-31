from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Colaborador, Cargo, Departamento
from django.contrib.auth.decorators import login_required


# Função para formatar CPF
def formataCPF(cpf):
    valorTratado = cpf.replace(".", "").replace("-", "")
    return valorTratado




@login_required
# lista os colaboradores cadastrados
def colaborador_lista(request):
    # Busca todos os colaboradores ordenados por nome
    colaboradores = Colaborador.objects.all().order_by("nome")

    # Inicializa as variáveis do filtro como vazias
    nome = ""
    matricula = ""
    cpf = ""
    cargo_id = ""
    departamento_id = ""
    situacao = ""
    data_admissao_inicial = ""
    data_admissao_final = ""
    data_desligamento_inicial = ""
    data_desligamento_final = ""


    if request.method == "POST":
        # Filtros
        # Obtém o valor do filtro retorna uma string vazia ("") caso não exista
        nome = request.POST.get("filtro-nome", "")
        if nome:
            colaboradores = colaboradores.filter(nome__icontains=nome)
        
        matricula = request.POST.get("filtro-matricula", "")
        if matricula:
            colaboradores = colaboradores.filter(matricula__icontains=matricula)
        
        cpf = formataCPF(request.POST.get("filtro-cpf", ""))
        if cpf:
            colaboradores = colaboradores.filter(cpf__icontains=cpf)
        
        cargo_id = request.POST.get("filtro-cargo", "")
        if cargo_id:
            cargo_id = int(cargo_id)
            colaboradores = colaboradores.filter(cargo=cargo_id)
        
        departamento_id = request.POST.get("filtro-departamento", "")
        if departamento_id:
            departamento_id = int(departamento_id)
            colaboradores = colaboradores.filter(departamento=departamento_id)
        
        situacao = request.POST.get("filtro-situacao", "")
        if situacao:
            colaboradores = colaboradores.filter(situacao=situacao)

        # Filtro por data de admissão
        data_admissao_inicial = request.POST.get("filtro-data_admissao_inicial", "")
        data_admissao_final = request.POST.get("filtro-data_admissao_final", "")

        if data_admissao_inicial:
            colaboradores = colaboradores.filter(admissao__gte=data_admissao_inicial)
        
        if data_admissao_final:
            colaboradores = colaboradores.filter(admissao__lte=data_admissao_final)

        # Filtro por data de desligamento
        data_desligamento_inicial = request.POST.get("filtro-data_desligamento_inicial", "")
        data_desligamento_final = request.POST.get("filtro-data_desligamento_final", "")

        if data_desligamento_inicial:
            colaboradores = colaboradores.filter(desligamento__gte=data_desligamento_inicial)
        
        if data_desligamento_final:
            colaboradores = colaboradores.filter(desligamento__lte=data_desligamento_final)
    

    # Calcula os valores para os cards
    total_colaboradores = colaboradores.count()
    total_ativos = colaboradores.filter(situacao="Ativo").count()
    total_afastados = colaboradores.filter(situacao="Afastado").count()
    total_demitidos = colaboradores.filter(situacao="Demitido").count()

  
     # Dados para template completo
    cargos = Cargo.objects.all().order_by("descricao")
    departamentos = Departamento.objects.all().order_by("descricao")
    situacoes = Colaborador._meta.get_field("situacao").choices
    return render(
        request,
        "colaboradores/colaborador_lista.html",
        {
            "colaboradores": colaboradores,
            "cargos": cargos,
            "departamentos": departamentos,
            "situacoes": situacoes,
            "filtro_nome": nome,
            "filtro_matricula": matricula,
            "filtro_cpf": cpf,
            "filtro_cargo": cargo_id,
            "filtro_departamento": departamento_id,
            "filtro_situacao": situacao,
            "filtro_data_admissao_inicial": data_admissao_inicial,
            "filtro_data_admissao_final": data_admissao_final,
            "filtro_data_desligamento_inicial": data_desligamento_inicial,
            "filtro_data_desligamento_final": data_desligamento_final,
            "total_colaboradores": total_colaboradores,
            "total_ativos": total_ativos,
            "total_afastados": total_afastados,
            "total_demitidos": total_demitidos,
        },
    )


# Cadastra um novo colaborador
def novoColaborador(request):
    # Verifica o metodo de envio dos dados
    if request.method == "POST":
        # Recupera os valores do formulário
        matricula = request.POST.get("matricula")
        cpf = formataCPF(request.POST.get("cpf"))
        nome = request.POST.get("nome").upper()
        cargo = request.POST.get("cargo")
        departamento = request.POST.get("departamento")
        data_admissao = request.POST.get("data_admissao")

        # Buscar os objetos Cargo e Departamento pelos IDs fornecidos
        cargo = Cargo.objects.get(id=cargo)
        departamento = Departamento.objects.get(id=departamento)

        # Tratamento de erros, verifica se o registro foi cadastrado com sucesso e exibe uma mensagem
        try:
            # Cria o novo colaborador no banco de dados
            cadastrar_colaborador = Colaborador(
                matricula=matricula,
                cpf=cpf,
                nome=nome,
                cargo=cargo,
                departamento=departamento,
                admissao=data_admissao,
            )

            # Salva o novo colaborador no banco de dados
            cadastrar_colaborador.save()

            messages.success(request, "Colaborador cadastrado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar o colaborador: {str(e)}")

        # Retorna para a lista de colaboradores
        return redirect("colaboradores_lista")


def editarColaborador(request, colaborador_id):
    # A função get_object_or_404 possui dois argumentos (TABELA DO BANCO E ID)
    # Caso a função encontre o ID na tabela o registro é retornado, caso o ID não seja encontrado ocorrera um erro 404
    colaborador = get_object_or_404(Colaborador, pk=colaborador_id)

    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário de edição
        nome = request.POST.get("nome").upper()
        matricula = request.POST.get("matricula")
        cpf = formataCPF(request.POST.get("cpf"))
        cargo = request.POST.get("cargo")
        departamento = request.POST.get("departamento")
        data_admissao = request.POST.get("data_admissao")
        data_desligamento = request.POST.get("data_desligamento")
        situacao = request.POST.get("situacao")

        # Busca os objetos Cargos e Departamentos pelos IDs fornecidos
        cargo = Cargo.objects.get(id=cargo)
        departamento = Departamento.objects.get(id=departamento)

        try:
            # Atualiza os dados do colaborador
            colaborador.nome = nome
            colaborador.matricula = matricula
            colaborador.cpf = cpf
            colaborador.cargo = cargo
            colaborador.departamento = departamento
            colaborador.admissao = data_admissao
            colaborador.situacao = situacao
            colaborador.desligamento = data_desligamento if data_desligamento else None

            # Salva as mudanças no banco de dados
            colaborador.save()

            # Mensagem e redirecionamento para tabela de colaboradores
            messages.success(request, "Colaborador atualizado com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao atualizar o colaborador: {str(e)}")

        # Retorna para a lista de colaboradores em caso de sucesso ou fracasso
        return redirect("colaboradores_lista")

    cargos = Cargo.objects.all()
    departamentos = Departamento.objects.all()
    situacoes = Colaborador._meta.get_field("situacao").choices

    return render(
        request,
        "colaboradores/editar_colaborador.html",
        {
            "colaborador": colaborador,
            "cargos": cargos,
            "departamentos": departamentos,
            "situacoes": situacoes,
        },
    )


def excluirColaborador(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        colaborador_id = request.POST.get("idColaborador")
        # Busca na tabela de colaboradores um ID igual ao ID enviado pelo modal
        colaborador = get_object_or_404(Colaborador, pk=colaborador_id)

        # Tenta Realizar a exclusão
        try:
            colaborador.delete()
            messages.success(request, "Colaborador excluído com sucesso!")
        # Execeção e tratamento de erros
        except Exception as e:
            messages.error(request, f"Erro ao excluir o colaborador: {str(e)}")
        
        # Redireciona para a lista de colaboradores
        return redirect("colaboradores_lista")
