from django.urls import path
from cadastros import views

urlpatterns = [
    # Urls Cadastros
    path("cadastros/", views.listaCadastros, name="lista_cadastros"),

    # Url Cargos
    path("novoCargo/", views.novoCargo, name="novo_cargo"),
    path("editarCargo/", views.editarCargo, name="editar_cargo"),
    path("excluirCargo/", views.excluirCargo, name="excluir_cargo"),

    # Url Departamentos
    path("novoDepartamento/", views.novoDepartamento, name="novo_departamento"),
    path("editarDepartamento/", views.editarDepartamento, name="editar_departamento"),
    path("excluirDepartamento/", views.excluirDepartamento, name="excluir_departamento"),

    # Urls Especialidades Fornecedores
    path("novaEspFornecedor/", views.novaEspFornecedor, name="nova_especialidade_fornecedor"),
    path("editarEspFornecedor/", views.editarEspFornecedor, name="editar_especialidade_fornecedor"),
    path("excluirEspFornecedor/", views.excluirEspFornecedor, name="excluir_especialidade_fornecedor"),

    # Urls Grupo Veiculos
    path("novoGrupoVeiculos/", views.novoGrupoVeiculo, name="novo_grupo_veiculo"),
    path("editarGrupoVeiculos/", views.editarGrupoVeiculo, name="editar_grupo_veiculo"),
    path("excluirGrupoVeiculos/", views.excluirGrupoVeiculo, name="excluir_grupo_veiculo"),
    
    # Urls Combustíveis
    path("novoCombustivel/", views.novoCombustivel, name="novo_combustivel"),
    path("editarCombustivel/", views.editarCombustivel, name="editar_combustivel"),
    path("excluirCombustivel/", views.excluirCombustivel, name="excluir_combustivel"),

    # Urls Causas manutenções
    path("novaCausa/", views.novaCausa, name="nova_causa"),
    path("editarCausa/", views.editarCausa, name="editar_causa"),
    path("excluirCausa/", views.excluirCausa, name="excluir_causa"),

    # Urls Tipos manutenções
    path("novoTipo/", views.novaTipo, name="novo_tipo"),
    path("editarTipo/", views.editarTipo, name="editar_tipo"),
    path("excluirTipo/", views.excluirTipo, name="excluir_tipo"),
    
    # Urls Centros de Custos
    path("novoCentroCusto/", views.novoCentroCusto, name="novo_centro_custo"),
    path("editarCentroCusto/", views.editarCentroCusto, name="editar_centro_custo"),
    path("excluirCentroCusto/", views.excluirCentroCusto, name="excluir_centro_custo"),

]
