from django.db import models
import datetime

# Create your models here.
class summarize_model(models.Model):
    text = models.TextField()
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text