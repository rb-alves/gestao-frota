from django.shortcuts import render, redirect, get_object_or_404
from .models import Fornecedor, EspecialidadeFornecedor
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Função de conversão de telefone
def formataTelefone(valor):
    valor = valor.replace('(', '').replace(') ', '').replace('-', '').strip()
    return valor

# Função de conversão de CNPJ
def formataCNPJ(valor):
    valor = valor.replace('.', '').replace('/', '').replace('-', '').strip()
    return valor

@login_required
# Lista os fornecedores cadastrados com filtros
def listaFornecedores(request):
    # Busca todos os fornecedores ordenados por nome
    fornecedores = Fornecedor.objects.all().order_by("nome")
    
    # Inicializa as variáveis do filtro como vazias
    nome = ""
    razao_social = ""
    cnpj = ""
    telefone = ""
    email = ""
    especialidade_id = ""

    if request.method == "POST":
        # Filtros
        # Filtro por nome
        nome = request.POST.get("filtro-nome", "")
        if nome:
            fornecedores = fornecedores.filter(nome__icontains=nome)
        
        # Filtro por razão social
        razao_social = request.POST.get("filtro-razao_social", "")
        if razao_social:
            fornecedores = fornecedores.filter(razao_social__icontains=razao_social)

        # Filtro por CNPJ
        cnpj = request.POST.get("filtro-cnpj", "")
        if cnpj:
            cnpj = formataCNPJ(cnpj)
            fornecedores = fornecedores.filter(cnpj__icontains=cnpj)

        # Filtro por telefone
        telefone = request.POST.get("filtro-telefone", "")
        if telefone:
            telefone = formataTelefone(telefone)
            fornecedores = fornecedores.filter(telefone__icontains=telefone)

        # Filtro por email
        email = request.POST.get("filtro-email", "")
        if email:
            fornecedores = fornecedores.filter(email__icontains=email)

        # Filtro por especialidade
        especialidade_id = request.POST.get("filtro-especialidade", "")
        if especialidade_id:
            especialidade_id = int(especialidade_id)
            fornecedores = fornecedores.filter(especialidade=especialidade_id)

    # Dados para o template
    especialidades = EspecialidadeFornecedor.objects.all().order_by("descricao")
    return render(
        request,
        "fornecedores/lista_fornecedores.html",
        {
            "fornecedores": fornecedores,
            "especialidades": especialidades,
            "filtro_nome": nome,
            "filtro_razao_social": razao_social,
            "filtro_cnpj": cnpj,
            "filtro_telefone": telefone,
            "filtro_email": email,
            "filtro_especialidade": especialidade_id,
        },
    )


# Cria um novo fornecedor na tabela e retorna a lista de fornecedores
def novoFornecedor(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        nome = request.POST.get("nome").upper()
        razao_social = request.POST.get("razao_social").upper()
        cnpj = formataCNPJ(request.POST.get("cnpj"))
        telefone = formataTelefone(request.POST.get("telefone"))
        email = request.POST.get("email")
        especialidade = request.POST.get("especialidade")

        # Busca os objeto especialidade pelo ID fornecido
        especialidade = (
            EspecialidadeFornecedor.objects.get(id=especialidade)
            if especialidade
            else None
        )

        # Tratamento de erros, verifica se o registro foi cadastrado com sucesso e exibe uma mensagem

        try:
            # Cria o novo fornecedor no banco de dados
            cadastrar_fornecedor = Fornecedor(
                nome=nome,
                razao_social=razao_social,
                cnpj=cnpj,
                telefone=telefone,
                email=email,
                especialidade=especialidade,
            )

            # Salva o colaborador no banco de dados
            cadastrar_fornecedor.save()

            messages.success(request, "Fornecedor cadastrado com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar o fornecedor: {str(e)}")

        # Retorna para a lista de colaboradores
        return redirect("lista_fornecedores")


def editarFornecedor(request, fornecedor_id):
    # A função get_object_or_404 possui dois argumentos (TABELA DO BANCO E ID)
    # Caso a função encontre o ID na tabela o registro é retornado, caso o ID não seja encontrado ocorrera um erro 404
    fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)

    # Verifica se o tipo de requisição é POST
    if request.method == "POST":
        nome = request.POST.get("nome").upper()
        razao_social = request.POST.get("razao_social").upper()
        cnpj = formataCNPJ(request.POST.get("cnpj"))
        telefone = formataTelefone(request.POST.get("telefone"))
        email = request.POST.get("email")
        especialidade = request.POST.get("especialidade")

        # Busca os objeto especialidade pelo ID fornecido
        especialidade = (
            EspecialidadeFornecedor.objects.get(id=especialidade)
            if especialidade
            else None
        )

        # Tenta realizar as alterações
        try:
            # Atualiza os dados do fornecedor
            fornecedor.nome = nome
            fornecedor.razao_social = razao_social
            fornecedor.cnpj = cnpj
            fornecedor.telefone = telefone
            fornecedor.email = email
            fornecedor.especialidade = especialidade

            # Salva as alteraçõe no banco de dados
            fornecedor.save()

            # Mensagem e redirecionamento para a lista de fornecedores
            messages.success(request, "Fornecedor atualizado com sucesso!")

        except Exception as e:
            # Exceção e tratamento de erros
            messages.error(request, f"Erro ao atualizar o fornecedor: {str(e)}")

        return redirect("lista_fornecedores")

    especialidades = EspecialidadeFornecedor.objects.all().order_by("descricao")
    return render(
        request,
        "fornecedores/editar_fornecedor.html",
        {"fornecedor": fornecedor, "especialidades": especialidades},
    )


# Exclui o fornecedor da tabela e retorna a lista de fornecedores
def excluirFornecedor(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        fornecedor_id = request.POST.get("idFornecedor")
        # Busca na tabela de colaboradores um ID igual ao ID enviado pelo modal
        fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)

        # Tenta realizar a exclusão
        try:
            fornecedor.delete()
            messages.success(request, "Fornecedor excluído com sucesso!")

        # Exceção e tratamento de erros
        except Exception as e:
            messages.error(request, f"Erro ao excluir o fornecedor {str(e)}")

        # Redireciona para a lista de fornecedores
        return redirect("lista_fornecedores")
