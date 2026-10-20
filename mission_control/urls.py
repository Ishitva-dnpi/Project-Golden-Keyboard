from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="api/v1/no-auth/missions/", permanent=False)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/no-auth/", include("auth_none.urls")),
    path("api/v1/basic-auth/", include("auth_basic.urls")),
    path("api/v1/session-auth/", include("auth_session.urls")),
    path("api/v1/token-auth/", include("auth_token_scheme.urls")),
    path("api/v1/jwt-auth/", include("auth_jwt.urls")),
]
