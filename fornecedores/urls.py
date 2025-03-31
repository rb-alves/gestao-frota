from django.urls import path
from fornecedores import views


urlpatterns = [
    path("fornecedores/", views.listaFornecedores, name="lista_fornecedores"),
    path("novoFornecedor/", views.novoFornecedor, name="novo_fornecedor"),
    path("excluirFornecedor/", views.excluirFornecedor, name="excluir_fornecedor"),
    path("editarFornecedor/<int:fornecedor_id>", views.editarFornecedor, name="editar_fornecedor",),
]
