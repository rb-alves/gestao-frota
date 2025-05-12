from django.urls import path
from seguranca import views


urlpatterns = [

    # Urls Segurança - Multas
    path("multas/", views.ListaMultas, name="lista_multas"),
    path("novaMulta/", views.novaMulta, name="nova_multa"),
    path("editarMulta/<int:multa_id>", views.editarMulta, name="editar_multa"),
    path("excluirMulta/", views.excluirMulta, name="excluir_multa"),

]
