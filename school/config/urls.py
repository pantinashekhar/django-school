"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# src/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView , SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Connect the Auth system (Fixes /accounts/login/ 404)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 2. Connect your Core app (Fixes /dashboard 404)
    # We leave the prefix empty "" so the core handles root '/' and '/dashboard'
    path('', include('core.urls', namespace='core')),

    path('academics/', include('academics.urls', namespace='academics')),

    path('accounts', RedirectView.as_view(url='/accounts/login/', permanent=True)), 
    path("api/v1/accounts/", include("accounts.api.urls", namespace="accounts_api")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/core/", include("core.api.urls", namespace="core_api")),
    path("api/v1/academics/", include("academics.api.urls", namespace="academics_api")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
