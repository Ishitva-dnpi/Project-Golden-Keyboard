from rest_framework.routers import DefaultRouter

from .views import BasicAuthMissionViewSet

router = DefaultRouter()
router.register("missions", BasicAuthMissionViewSet, basename="basic-auth-mission")

urlpatterns = router.urls
