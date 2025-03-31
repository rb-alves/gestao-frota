from django.shortcuts import render, redirect, get_object_or_404
from colaboradores.models import Cargo, Departamento
from fornecedores.models import EspecialidadeFornecedor
from frota.models import GrupoVeiculo, Combustivel, Causa, Tipo, CentroCusto
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def listaCadastros(request):
    cargos = Cargo.objects.all().order_by("descricao")
    departamentos = Departamento.objects.all().order_by("descricao")
    especialidades_fornecedores = EspecialidadeFornecedor.objects.all().order_by(
        "descricao"
    )
    grupo_veiculos = GrupoVeiculo.objects.all().order_by("descricao")
    combustiveis = Combustivel.objects.all().order_by("descricao")
    causas = Causa.objects.all().order_by('descricao')
    tipos = Tipo.objects.all().order_by('descricao')
    centros = CentroCusto.objects.all().order_by('descricao')
    return render(
        request,
        "cadastros/lista_cadastros.html",
        {
            "cargos": cargos,
            "departamentos": departamentos,
            "especialiadesFornecedores": especialidades_fornecedores,
            "grupos_veiculos": grupo_veiculos,
            "combustiveis": combustiveis,
            "causas": causas,
            "tipos": tipos,
            "centros": centros
        }
    )


########################################## CARGOS ##############################################
# Cadastra um novo cargo
def novoCargo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        descricao = request.POST.get("descricaoCargo")

        # Verifica se o campo descrição foi enviado vazio
        if descricao != "":
            # Tenta cadstrar um novo cargo
            try:
                # Cria um novo cargo no banco de dados
                cadastrar_cargo = Cargo(descricao=descricao)

                # Salva as alterações
                cadastrar_cargo.save()
                messages.success(request, "Cargo cadastrado com sucesso")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar o cargo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao cadastrar o cargo: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Edita um cargo existente
def editarCargo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de edição
        cargo_id = request.POST.get("idCargoEdit")
        descricao = request.POST.get("descricaoCargoEdit")

        if descricao != "":
            try:
                # Busca na tabela de cargos um ID igual ao ID enviado pelo modal
                cargo = get_object_or_404(Cargo, pk=cargo_id)

                # Altera os dados no banco de dados
                cargo.descricao = descricao

                # Salva os dados no banco de dados
                cargo.save()
                messages.success(request, "Cargo atualizado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao atualizar o cargo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao atualizar o cargo: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Exclui um cargo existente
def excluirCargo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        cargo_id = request.POST.get("idCargoDel")

        try:
            # Busca na tabela de cargos um ID igual ao ID enviado pelo modal
            cargo = get_object_or_404(Cargo, pk=cargo_id)
            cargo.delete()
            messages.success(request, "Cargo excluído com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao excluir o cargo: {str(e)}")

        return redirect("lista_cadastros")


########################################## DEPARTAMENTOS ##############################################
# Cadastra um novo departamento
def novoDepartamento(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        descricao = request.POST.get("descricaoDepartamento")

        # Verifica se o campo descrição foi enviado vazio
        if descricao != "":
            # Tenta cadstrar um novo Departamento
            try:
                # Cria um novo departamento no banco de dados
                cadastrar_departamento = Departamento(descricao=descricao)

                # Salva as alterações
                cadastrar_departamento.save()
                messages.success(request, "Departamento cadastrado com sucesso")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar o departamento: {str(e)}")
        else:
            messages.error(
                request,
                "Erro ao cadastrar o departamento: O campo descrição está vazio",
            )

        return redirect("lista_cadastros")


# Edita um departamento existente
def editarDepartamento(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de edição
        departamento_id = request.POST.get("idDepartamentoEdit")
        descricao = request.POST.get("descricaoDepartamentoEdit")

        if descricao != "":
            try:
                # Busca na tabela de departamentos um ID igual ao ID enviado pelo modal
                departamento = get_object_or_404(Departamento, pk=departamento_id)

                # Altera os dados no banco de dados
                departamento.descricao = descricao

                # Salva os dados no banco de dados
                departamento.save()
                messages.success(request, "Departamento atualizado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao atualizar o departamento: {str(e)}")
        else:
            messages.error(
                request,
                "Erro ao atualizar o departamento: O campo descrição está vazio",
            )

        return redirect("lista_cadastros")


# Exclui um departamento existente
def excluirDepartamento(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        departamento_id = request.POST.get("idDepartamentoDel")

        try:
            # Busca na tabela de departamentos um ID igual ao ID enviado pelo modal
            departamento = get_object_or_404(Departamento, pk=departamento_id)
            departamento.delete()
            messages.success(request, "Departamento excluído com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao excluir o departamento: {str(e)}")

        return redirect("lista_cadastros")


########################################## ESPECIALIDADE DOS FORNECEDORES ##############################################
# Cadastra uma novo especialidade
def novaEspFornecedor(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        descricao = request.POST.get("descricaoEspFornecedor")

        # Verifica se o campo descrição foi enviado vazio
        if descricao != "":
            # Tenta cadstrar uma nova especialidade
            try:
                # Cria uma nova especialidade no banco de dados
                cadastrar_especialidade = EspecialidadeFornecedor(descricao=descricao)

                # Salva as alterações
                cadastrar_especialidade.save()
                messages.success(request, "Especialidade cadastrada com sucesso")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar a especialidade: {str(e)}")
        else:
            messages.error(
                request,
                "Erro ao cadastrar a especialidade: O campo descrição está vazio",
            )

        return redirect("lista_cadastros")


# Edita um especialidade existente
def editarEspFornecedor(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de edição
        especialidade_id = request.POST.get("idEspFornecedorEdit")
        descricao = request.POST.get("descricaoEspFornecedorEdit")

        if descricao != "":
            try:
                # Busca na tabela de especialidades fornecedores um ID igual ao ID enviado pelo modal
                especialidade = get_object_or_404(
                    EspecialidadeFornecedor, pk=especialidade_id
                )

                # Altera os dados no banco de dados
                especialidade.descricao = descricao

                # Salva os dados no banco de dados
                especialidade.save()
                messages.success(request, "Especialidade atualizada com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao atualizar a especialidade: {str(e)}")
        else:
            messages.error(
                request,
                "Erro ao atualizar a especialidade: O campo descrição está vazio",
            )

        return redirect("lista_cadastros")


# Exclui uma especialidade existente
def excluirEspFornecedor(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        especialidade_id = request.POST.get("idEspFornecedoresDel")

        try:
            # Busca na tabela de especialidade um ID igual ao ID enviado pelo modal
            especialidade = get_object_or_404(
                EspecialidadeFornecedor, pk=especialidade_id
            )
            especialidade.delete()
            messages.success(request, "Especialidade excluída com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao excluir a especialidade: {str(e)}")

        return redirect("lista_cadastros")


########################################## GRUPO DE VEÍCULOS ##############################################
# Cadastra um novo grupo
def novoGrupoVeiculo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        descricao = request.POST.get("descricaogrupoVeiculo")

        # Verifica se o campo descrição foi enviado vazio
        if descricao != "":
            # Tenta cadstrar um novo grupo
            try:
                # Cria um novo grupo no banco de dados
                cadastrar_grupo = GrupoVeiculo(descricao=descricao)

                # Salva as alterações
                cadastrar_grupo.save()
                messages.success(request, "Grupo cadastrado com sucesso")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar o grupo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao cadastrar o grupo: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Edita um grupo existente
def editarGrupoVeiculo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de edição
        grupo_id = request.POST.get("idgrupoVeiculoEdit")
        descricao = request.POST.get("descricaogrupoVeiculoEdit")

        if descricao != "":
            try:
                # Busca na tabela de grupos um ID igual ao ID enviado pelo modal
                grupo = get_object_or_404(GrupoVeiculo, pk=grupo_id)

                # Altera os dados no banco de dados
                grupo.descricao = descricao

                # Salva os dados no banco de dados
                grupo.save()
                messages.success(request, "Grupo atualizado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao atualizar o grupo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao atualizar o grupo: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Exclui um grupo existente
def excluirGrupoVeiculo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        grupo_id = request.POST.get("idgrupoVeiculoDel")

        try:
            # Busca na tabela de gruposs um ID igual ao ID enviado pelo modal
            grupo = get_object_or_404(GrupoVeiculo, pk=grupo_id)
            grupo.delete()
            messages.success(request, "Grupo excluído com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao excluir o Grupo: {str(e)}")

        return redirect("lista_cadastros")


########################################## COMBUSTIVEL ##############################################
# Cadastra um novo combustível
def novoCombustivel(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        descricao = request.POST.get("descricaocombustivel")

        # Verifica se o campo descrição foi enviado vazio
        if descricao != "":
            # Tenta cadstrar um novo combustivel
            try:
                # Cria um novo combustivel no banco de dados
                cadastrar_combustivel = Combustivel(descricao=descricao)

                # Salva as alterações
                cadastrar_combustivel.save()
                messages.success(request, "Combustivel cadastrado com sucesso")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar o combustivel: {str(e)}")
        else:
            messages.error(
                request, "Erro ao cadastrar o combustivel: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Edita um combustivel existente
def editarCombustivel(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de edição
        combustivel_id = request.POST.get("idcombustivelEdit")
        descricao = request.POST.get("descricaocombustivelEdit")

        if descricao != "":
            try:
                # Busca na tabela de combustiveis um ID igual ao ID enviado pelo modal
                combustivel = get_object_or_404(Combustivel, pk=combustivel_id)

                # Altera os dados no banco de dados
                combustivel.descricao = descricao

                # Salva os dados no banco de dados
                combustivel.save()
                messages.success(request, "Combustível atualizado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao atualizar o combustível: {str(e)}")
        else:
            messages.error(
                request, "Erro ao atualizar o combustível: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Exclui um combustível existente
def excluirCombustivel(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        combustivel_id = request.POST.get("idcombustivelDel")

        try:
            # Busca na tabela de combustiveis um ID igual ao ID enviado pelo modal
            combustivel = get_object_or_404(Combustivel, pk=combustivel_id)
            combustivel.delete()
            messages.success(request, "Combustível excluído com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao excluir o combustível: {str(e)}")

        return redirect("lista_cadastros")


########################################## CAUSA DAS MANUTENÇÕES ##############################################

# Cadastra uma nova causa
def novaCausa(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        descricao = request.POST.get("descricaoCausa")

        # Verifica se o campo descrição foi enviado vazio
        if descricao != "":
            # Tenta cadstrar uma nova causa
            try:
                # Cria uma nova causa no banco de dados
                cadastrar_causa = Causa(descricao=descricao)

                # Salva as alterações
                cadastrar_causa.save()
                messages.success(request, "Causa cadastrada com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar a causa: {str(e)}")
        else:
            messages.error(
                request, "Erro ao cadastrar a causa: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Edita uma causa existente
def editarCausa(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de edição
        causa_id = request.POST.get("idCausaEdit")
        descricao = request.POST.get("descricaoCausaEdit")

        if descricao != "":
            try:
                # Busca na tabela de causas um ID igual ao ID enviado pelo modal
                causa = get_object_or_404(Causa, pk=causa_id)

                # Altera os dados no banco de dados
                causa.descricao = descricao

                # Salva os dados no banco de dados
                causa.save()
                messages.success(request, "Causa atualizada com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao atualizar a causa: {str(e)}")
        else:
            messages.error(
                request, "Erro ao atualizar a causa: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Exclui uma causa existente
def excluirCausa(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        causa_id = request.POST.get("idCausaDel")

        try:
            # Busca na tabela de causas um ID igual ao ID enviado pelo modal
            causa = get_object_or_404(Causa, pk=causa_id)
            causa.delete()
            messages.success(request, "Causa excluída com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao excluir a causa: {str(e)}")

        return redirect("lista_cadastros")


########################################## TIPO DAS MANUTENÇÕES ##############################################

# Cadastra um novo tipo de manutenção
def novaTipo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        descricao = request.POST.get("descricaoTipo")

        # Verifica se o campo descrição foi enviado vazio
        if descricao != "":
            # Tenta cadstrar um novo tipo
            try:
                # Cria um novo tipo no banco de dados
                cadastrar_tipo = Tipo(descricao=descricao)

                # Salva as alterações
                cadastrar_tipo.save()
                messages.success(request, "Tipo cadastrado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar o tipo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao cadastrar o tipo: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Edita um tipo existente
def editarTipo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de edição
        tipo_id = request.POST.get("idTipoEdit")
        descricao = request.POST.get("descricaoTipoEdit")

        if descricao != "":
            try:
                # Busca na tabela de tipos um ID igual ao ID enviado pelo modal
                tipo = get_object_or_404(Tipo, pk=tipo_id)

                # Altera os dados no banco de dados
                tipo.descricao = descricao

                # Salva os dados no banco de dados
                tipo.save()
                messages.success(request, "Tipo atualizado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao atualizar o tipo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao atualizar o tipo: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Exclui um tipo existente
def excluirTipo(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        tipo_id = request.POST.get("idTipoDel")

        try:
            # Busca na tabela de tipos um ID igual ao ID enviado pelo modal
            tipo = get_object_or_404(Tipo, pk=tipo_id)
            tipo.delete()
            messages.success(request, "Tipo excluído com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao excluir a tipo: {str(e)}")

        return redirect("lista_cadastros")



########################################## CENTROS DE CUSTOS ##############################################

# Cadastra uma novo centro de custo
def novoCentroCusto(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores do formulário
        descricao = request.POST.get("descricaoCentroCusto")

        # Verifica se o campo descrição foi enviado vazio
        if descricao != "":
            # Tenta cadstrar um novo centro de custo
            try:
                # Cria uma novo centro de custo no banco de dados
                cadastrar_centro = CentroCusto(descricao=descricao)

                # Salva as alterações
                cadastrar_centro.save()
                messages.success(request, "Centro de Custo cadastrado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar o centro de custo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao cadastrar o centro de custo: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Edita um centro de custo existente
def editarCentroCusto(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de edição
        centro_id = request.POST.get("idCentroCustoEdit")
        descricao = request.POST.get("descricaoCentroCustoEdit")

        if descricao != "":
            try:
                # Busca na tabela de centros de custos um ID igual ao ID enviado pelo modal
                centro = get_object_or_404(CentroCusto, pk=centro_id)

                # Altera os dados no banco de dados
                centro.descricao = descricao

                # Salva os dados no banco de dados
                centro.save()
                messages.success(request, "Cemtro de custo atualizado com sucesso!")

            except Exception as e:
                messages.error(request, f"Erro ao atualizar o centro de custo: {str(e)}")
        else:
            messages.error(
                request, "Erro ao atualizar o centro de custo: O campo descrição está vazio"
            )

        return redirect("lista_cadastros")


# Exclui um centro de custo existente
def excluirCentroCusto(request):
    # Verifica se a requisição é do tipo POST
    if request.method == "POST":
        # Recupera os valores ocultos no modal de exclusão
        centro_id = request.POST.get("idCentroCustoDel")

        try:
            # Busca na tabela de centro de custo um ID igual ao ID enviado pelo modal
            centro = get_object_or_404(CentroCusto, pk=centro_id)
            centro.delete()
            messages.success(request, "Centro de custo excluído com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao excluir o centro de custo: {str(e)}")

        return redirect("lista_cadastros")

