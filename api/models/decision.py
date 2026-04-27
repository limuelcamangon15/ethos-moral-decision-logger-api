from django.db import models

class Decision(models.Model):
    title = models.CharField(max_length=255)
    context = models.TextField()
    chosen_action = models.TextField()
    reasoning = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title