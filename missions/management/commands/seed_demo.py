from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from missions.models import Mission


class Command(BaseCommand):
    help = "Creates a demo user (for Basic/Session/Token/JWT auth) and sample missions."

    def handle(self, *args, **options):
        username, password = "player_one", "hunter2pass"

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created demo user: {username} / {password}"))
        else:
            self.stdout.write(f"Demo user already exists: {username} / {password}")

        if not Mission.objects.exists():
            now = timezone.now()
            Mission.objects.bulk_create([
                Mission(
                    codename="Binary Search & Destroy",
                    brief="Find the target in a rotated sorted array.",
                    points=100,
                    difficulty="warmup",
                    status="unclaimed",
                    deadline=now + timedelta(days=2),
                ),
                Mission(
                    codename="Segfault Safari",
                    brief="Track down a use-after-free bug in the given C snippet.",
                    points=250,
                    difficulty="core",
                    status="in_progress",
                    hostel="krishna_bhawan",
                    deadline=now + timedelta(days=1),
                ),
                Mission(
                    codename="The Final Byte",
                    brief="Reverse-engineer the obfuscated binary to recover the flag.",
                    points=500,
                    difficulty="boss_level",
                    status="cracked",
                    hostel="vyas_bhawan",
                    solver_handle="packet_ninja",
                    deadline=now - timedelta(hours=3),
                ),
            ])
            self.stdout.write(self.style.SUCCESS("Seeded 3 sample missions."))
        else:
            self.stdout.write("Missions already exist, skipping seed data.")
