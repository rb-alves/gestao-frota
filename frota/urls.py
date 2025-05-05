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

    # Urls Frota - Manutenções Veiculos
    path("manutencoesVeiculos/", views.listaManutencoes, name="lista_manutencoes_veiculos"),
    path("novaManutencaoVeiculo/", views.novaManutVeiculo, name="nova_manutencao_veiculo"),
    path("editarManutencaoVeiculo/<int:manutencao_id>", views.editarManutVeiculo, name="editar_manutencao_veiculo"),
    path("excluirManutencaoVeiculo/", views.excluiManutVeiculo, name="excluir_manutencao_veiculo"),

    # Urls Frota - Manutenções Maquinas
    path("manutencoesMaquinas/", views.listaManutencoesMaquinas, name="lista_manutencoes_maquinas"),
    path("novaManutencaoMaquina/", views.novaManutMaquina, name="nova_manutencao_maquina"),
    path("editarManutencaoMaquina/<int:manutencao_id>", views.editarManutMaquina, name="editar_manutencao_maquina"),
    path("excluirManutencaoMaquina/", views.excluiManutMaquina, name="excluir_manutencao_maquina"),

]
