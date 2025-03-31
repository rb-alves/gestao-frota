from django.urls import path
from frota import views

urlpatterns = [

    # Urls Frota - Veiculos
    path("veiculos/", views.listaVeiculos, name="lista_veiculos"),
    path("novoVeiculo/", views.novoVeiculo, name="novo_veiculo"),
    path("editarVeiculo/<int:veiculo_id>", views.editarVeiculo, name="editar_veiculo"),
    path("excluirVeiculo/", views.excluirVeiculo, name="excluir_veiculo"),

    # Urls Frota - Maquinas
    path("maquinas/", views.listaMaquinas, name="lista_maquinas"),
    path("novaMaquina/", views.novaMaquina, name="nova_maquina"),
    path("editarMaquina/<int:maquina_id>", views.editarMaquina, name="editar_maquina"),
    path("excluirMaquina/", views.excluirMaquina, name="excluir_maquina"),

]
