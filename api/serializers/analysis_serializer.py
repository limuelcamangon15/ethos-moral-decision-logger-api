from rest_framework import serializers
from api.models import Analysis

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = [
            "ethics",
            "risk_level",
            "time_scope",
            "affected_party",
            "justification_quality",
            "confidence",
            "explanation"
        ]