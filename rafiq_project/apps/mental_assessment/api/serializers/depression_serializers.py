
from ...models import DepressionTestResult
from rest_framework import serializers

class DepressionTestSerializer(serializers.Serializer):
    GENDER_MAP = {"Male": 0, "Female": 1}
    YES_NO_MAP = {"No": 0, "Yes": 1}
    SLEEP_MAP = {
        "Less than 5 hours": 3,
        "5-6 hours": 5.5,
        "7-8 hours": 7.5,
        "More than 8 hours": 10
    }
    DIET_MAP = {"Unhealthy": 0, "Moderate": 2.5, "Healthy": 5}

    gender = serializers.CharField()
    age = serializers.IntegerField()
    work_pressure = serializers.IntegerField()
    job_satisfaction = serializers.IntegerField()
    sleep_duration = serializers.CharField()
    dietary_habits = serializers.CharField()
    suicidal_thoughts = serializers.CharField()
    work_hours = serializers.IntegerField()
    financial_stress = serializers.IntegerField()
    family_history = serializers.CharField()

    def validate_gender(self, v):
        if v not in self.GENDER_MAP:
            raise serializers.ValidationError(f"Gender must be one of {list(self.GENDER_MAP.keys())}")
        return self.GENDER_MAP[v]

    def validate_age(self, v):
        if not (1 <= v <= 100):
            raise serializers.ValidationError("Age must be between 1 and 100")
        return v

    def validate_work_pressure(self, v):
        if not (1 <= v <= 5):
            raise serializers.ValidationError("Work pressure must be 1–5")
        return v

    def validate_job_satisfaction(self, v):
        if not (1 <= v <= 5):
            raise serializers.ValidationError("Job satisfaction must be 1–5")
        return v

    def validate_sleep_duration(self, v):
        if v not in self.SLEEP_MAP:
            raise serializers.ValidationError(f"Sleep duration must be one of {list(self.SLEEP_MAP.keys())}")
        return self.SLEEP_MAP[v]

    def validate_dietary_habits(self, v):
        if v not in self.DIET_MAP:
            raise serializers.ValidationError(f"Dietary habits must be one of {list(self.DIET_MAP.keys())}")
        return self.DIET_MAP[v]

    def validate_suicidal_thoughts(self, v):
        if v not in self.YES_NO_MAP:
            raise serializers.ValidationError(f"Suicidal thoughts must be one of {list(self.YES_NO_MAP.keys())}")
        return self.YES_NO_MAP[v]

    def validate_work_hours(self, v):
        if not (0 <= v <= 12):
            raise serializers.ValidationError("Work hours must be 0–12")
        return v

    def validate_financial_stress(self, v):
        if not (1 <= v <= 5):
            raise serializers.ValidationError("Financial stress must be 1–5")
        return v

    def validate_family_history(self, v):
        if v not in self.YES_NO_MAP:
            raise serializers.ValidationError(f"Family history must be one of {list(self.YES_NO_MAP.keys())}")
        return self.YES_NO_MAP[v]
