import base64
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from missions.models import Mission


class MissionModelValidationTests(APITestCase):
    def setUp(self):
        self.now = timezone.now()

    def test_unclaimed_cannot_have_hostel_or_solver(self):
        mission = Mission(
            codename="Stealth Sweep",
            brief="Find hidden keys",
            points=100,
            difficulty="warmup",
            status="unclaimed",
            hostel="ashok_bhawan",
            deadline=self.now + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            mission.clean()

    def test_cracked_mission_requires_hostel_and_solver(self):
        mission = Mission(
            codename="Matrix Infiltration",
            brief="Bypass sandbox",
            points=300,
            difficulty="boss_level",
            status="cracked",
            hostel="vyas_bhawan",
            solver_handle="",
            deadline=self.now + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            mission.clean()


class MissionAPITests(APITestCase):
    def setUp(self):
        self.now = timezone.now()
        self.user = User.objects.create_user(username="testplayer", password="testpassword123")
        self.mission = Mission.objects.create(
            codename="Initial Mission",
            brief="Analyze source code",
            points=150,
            difficulty="core",
            status="unclaimed",
            deadline=self.now + timedelta(days=2),
        )

    def test_no_auth_api(self):
        res = self.client.get("/api/v1/no-auth/missions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = {
            "codename": "New No-Auth Mission",
            "brief": "Find memory leak",
            "points": 200,
            "difficulty": "core",
            "status": "unclaimed",
            "deadline": (self.now + timedelta(days=3)).isoformat(),
        }
        res = self.client.post("/api/v1/no-auth/missions/", data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_basic_auth_api(self):
        res = self.client.get("/api/v1/basic-auth/missions/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        auth_header = "Basic " + base64.b64encode(b"testplayer:testpassword123").decode("ascii")
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)
        res = self.client.get("/api/v1/basic-auth/missions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_token_auth_api(self):
        res = self.client.get("/api/v1/token-auth/missions/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.post(
            "/api/v1/token-auth/login/",
            {"username": "testplayer", "password": "testpassword123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = res.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        res = self.client.get("/api/v1/token-auth/missions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_jwt_auth_api(self):
        res = self.client.get("/api/v1/jwt-auth/missions/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.post(
            "/api/v1/jwt-auth/login/",
            {"username": "testplayer", "password": "testpassword123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        access_token = res.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        res = self.client.get("/api/v1/jwt-auth/missions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.credentials()
