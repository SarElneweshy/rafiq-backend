
from ...models import DepressionTestResult
from rest_framework import serializers

class DepressionTestSerializer(serializers.Serializer):
    gender = serializers.IntegerField()
    age = serializers.IntegerField()
    work_pressure = serializers.IntegerField()
    job_satisfaction = serializers.IntegerField()
    sleep_duration = serializers.FloatField()
    dietary_habits = serializers.FloatField()
    suicidal_thoughts = serializers.IntegerField()
    work_hours = serializers.IntegerField()
    financial_stress = serializers.IntegerField()
    family_history = serializers.IntegerField()

    def validate_gender(self, v):
        if v not in [0, 1]:
            raise serializers.ValidationError("Gender must be 0 (Male) or 1 (Female)")
        return v

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
        if v not in [3, 5.5, 7.5, 10]:
            raise serializers.ValidationError("Invalid sleep duration")
        return v

    def validate_dietary_habits(self, v):
        if v not in [0, 2.5, 5]:
            raise serializers.ValidationError("Invalid dietary habits")
        return v

    def validate_suicidal_thoughts(self, v):
        if v not in [0, 1]:
            raise serializers.ValidationError("Must be 0 or 1")
        return v

    def validate_work_hours(self, v):
        if not (0 <= v <= 12):
            raise serializers.ValidationError("Work hours must be 0–12")
        return v

    def validate_financial_stress(self, v):
        if not (1 <= v <= 5):
            raise serializers.ValidationError("Financial stress must be 1–5")
        return v

    def validate_family_history(self, v):
        if v not in [0, 1]:
            raise serializers.ValidationError("Must be 0 or 1")
        return v
