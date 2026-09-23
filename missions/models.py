from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


HOSTEL_CHOICES = [
    ("ashok_bhawan", "Ashok Bhawan"),
    ("bhagirath_bhawan", "Bhagirath Bhawan"),
    ("budh_bhawan", "Budh Bhawan"),
    ("cv_raman_bhawan", "C.V. Raman Bhawan"),
    ("gandhi_bhawan", "Gandhi Bhawan"),
    ("krishna_bhawan", "Krishna Bhawan"),
    ("malaviya_bhawan_a", "Malaviya Bhawan-A"),
    ("malaviya_bhawan_b", "Malaviya Bhawan-B"),
    ("malaviya_bhawan_c", "Malaviya Bhawan-C"),
    ("malaviya_apartments", "Malaviya Apartments"),
    ("rana_pratap_bhawan", "Rana Pratap Bhawan"),
    ("ram_bhawan", "Ram Bhawan"),
    ("shankar_bhawan", "Shankar Bhawan"),
    ("sr_bhawan", "Srinivasa Ramanujan (SR) Bhawan"),
    ("vishwakarma_bhawan", "Vishwakarma Bhawan"),
    ("vyas_bhawan", "Vyas Bhawan"),
    ("meera_bhawan", "Meera Bhawan"),
]

DIFFICULTY_CHOICES = [
    ("warmup", "Warmup"),
    ("core", "Core"),
    ("boss_level", "Boss Level"),
]

STATUS_CHOICES = [
    ("unclaimed", "Unclaimed"),
    ("in_progress", "In Progress"),
    ("cracked", "Cracked"),
    ("expired", "Expired"),
]


class Mission(models.Model):
    codename = models.CharField(max_length=150)
    brief = models.TextField()
    points = models.IntegerField(validators=[MinValueValidator(0)])
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unclaimed")
    hostel = models.CharField(max_length=40, choices=HOSTEL_CHOICES, blank=True, null=True)
    solver_handle = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.DateTimeField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.codename} [{self.status}]"

    def clean(self):
        errors = {}

        if self.status == "unclaimed" and (self.hostel or self.solver_handle):
            errors["status"] = (
                "An unclaimed mission cannot already have a hostel or solver_handle."
            )

        if self.status in ("in_progress", "cracked") and not self.hostel:
            errors["hostel"] = f"A mission with status '{self.status}' must have a claiming hostel."

        if self.status == "cracked" and not self.solver_handle:
            errors["solver_handle"] = "A cracked mission must record who solved it (solver_handle)."

        if errors:
            raise ValidationError(errors)
