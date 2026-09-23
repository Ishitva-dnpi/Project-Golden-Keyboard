from rest_framework import serializers

from .models import Mission


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            "id",
            "codename",
            "brief",
            "points",
            "difficulty",
            "status",
            "hostel",
            "solver_handle",
            "deadline",
        ]

    def validate_points(self, value):
        if value < 0:
            raise serializers.ValidationError("points cannot be negative.")
        return value

    def validate_codename(self, value):
        if not value.strip():
            raise serializers.ValidationError("codename cannot be blank.")
        return value

    def validate(self, attrs):
        status = attrs.get("status", getattr(self.instance, "status", "unclaimed"))
        hostel = attrs.get("hostel", getattr(self.instance, "hostel", None))
        solver_handle = attrs.get("solver_handle", getattr(self.instance, "solver_handle", None))

        if status == "unclaimed" and (hostel or solver_handle):
            raise serializers.ValidationError(
                "An unclaimed mission cannot already have a hostel or solver_handle."
            )

        if status in ("in_progress", "cracked") and not hostel:
            raise serializers.ValidationError(
                {"hostel": f"A mission with status '{status}' must have a claiming hostel."}
            )

        if status == "cracked" and not solver_handle:
            raise serializers.ValidationError(
                {"solver_handle": "A cracked mission must record who solved it (solver_handle)."}
            )

        return attrs
