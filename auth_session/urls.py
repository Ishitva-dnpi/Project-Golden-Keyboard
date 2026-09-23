from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SessionAuthMissionViewSet, SessionLoginView, SessionLogoutView

router = DefaultRouter()
router.register("missions", SessionAuthMissionViewSet, basename="session-auth-mission")

urlpatterns = [
    path("login/", SessionLoginView.as_view(), name="session-login"),
    path("logout/", SessionLogoutView.as_view(), name="session-logout"),
] + router.urls
