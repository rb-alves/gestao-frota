from django.urls import path
from colaboradores import views

urlpatterns = [
    path("colaboradores/", views.colaborador_lista, name="colaboradores_lista"),
    path("novoColaborador/", views.novoColaborador, name="novo_colaborador"),
    path("editarColaborador/<int:colaborador_id>", views.editarColaborador, name="editar_colaborador",),
    path("excluirColaborador/", views.excluirColaborador, name="excluir_colaborador"),
]
