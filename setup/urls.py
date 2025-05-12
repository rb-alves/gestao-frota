from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Url Admin
    path("admin/", admin.site.urls),


    # Url Home
    path("", include("home.urls")),

    # Urls Colaboradores
    path("", include("colaboradores.urls")),

    # Urls Fornecedores
    path("", include("fornecedores.urls")),

    # Urls Cadastros
    path("", include("cadastros.urls")),

    # Urls Frota
    path("", include("frota.urls")),

    # Urls Login e Logout
    path('accounts/', include('allauth.urls')),

    # Urls Segurança
    path("", include("seguranca.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    