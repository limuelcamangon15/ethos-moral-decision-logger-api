from rest_framework import serializers
from api.models import Decision

class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decision
        fields = ["id", "title", "context", "chosen_action", "reasoning", "created_at"]