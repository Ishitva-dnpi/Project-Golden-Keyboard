from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import JWTAuthMissionViewSet

router = DefaultRouter()
router.register("missions", JWTAuthMissionViewSet, basename="jwt-auth-mission")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
] + router.urls
