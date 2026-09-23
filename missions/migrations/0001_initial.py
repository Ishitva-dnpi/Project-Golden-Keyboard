import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Mission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codename", models.CharField(max_length=150)),
                ("brief", models.TextField()),
                ("points", models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                (
                    "difficulty",
                    models.CharField(
                        choices=[("warmup", "Warmup"), ("core", "Core"), ("boss_level", "Boss Level")],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("unclaimed", "Unclaimed"),
                            ("in_progress", "In Progress"),
                            ("cracked", "Cracked"),
                            ("expired", "Expired"),
                        ],
                        default="unclaimed",
                        max_length=20,
                    ),
                ),
                (
                    "hostel",
                    models.CharField(
                        blank=True,
                        choices=[
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
                        ],
                        max_length=40,
                        null=True,
                    ),
                ),
                ("solver_handle", models.CharField(blank=True, max_length=100, null=True)),
                ("deadline", models.DateTimeField()),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]
