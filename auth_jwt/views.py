from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from missions.models import Mission
from missions.serializers import MissionSerializer


class JWTAuthMissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
