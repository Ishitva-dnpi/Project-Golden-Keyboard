from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from missions.models import Mission
from missions.serializers import MissionSerializer


class NoAuthMissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
