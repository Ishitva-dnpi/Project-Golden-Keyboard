from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TokenAuthMissionViewSet, TokenLoginView

router = DefaultRouter()
router.register("missions", TokenAuthMissionViewSet, basename="token-auth-mission")

urlpatterns = [
    path("login/", TokenLoginView.as_view(), name="token-login"),
] + router.urls
