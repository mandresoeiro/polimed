from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")), Versão do Django
    path("contas/", include("contas.urls")),  # url do app de contas
    path("perfil/", include("perfil.urls")),  # url do app de perfil
    path("config/", include("config.urls")),  # url do app de config
    path("", include("pages.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
