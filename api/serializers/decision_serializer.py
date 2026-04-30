from rest_framework import serializers
from api.models import Decision
from api.serializers.analysis_serializer import AnalysisSerializer

class DecisionSerializer(serializers.ModelSerializer):
    analysis = AnalysisSerializer(read_only=True)
    
    class Meta:
        model = Decision
        fields = ["id", "title", "context", "chosen_action", "reasoning", "created_at", "analysis"]