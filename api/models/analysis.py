from django.db import models
from .decision import Decision

class Analysis(models.Model):
    decision = models.OneToOneField(Decision, on_delete=models.CASCADE, related_name="analysis")
    ethics = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=50)
    time_scope = models.CharField(max_length=50)
    affected_party = models.CharField(max_length=50)

    justification_quality = models.FloatField()
    confidence = models.FloatField()

    explanation = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)