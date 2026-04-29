from django.db import models
from django.contrib.auth.models import User

class Decision(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="decisions")

    title = models.CharField(max_length=255)
    context = models.TextField()
    chosen_action = models.TextField()
    reasoning = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title