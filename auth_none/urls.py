from rest_framework.routers import DefaultRouter

from .views import NoAuthMissionViewSet

router = DefaultRouter()
router.register("missions", NoAuthMissionViewSet, basename="no-auth-mission")

urlpatterns = router.urls
