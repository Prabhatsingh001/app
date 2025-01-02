from django.db import models
from django.conf import settings

class Notes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sem = models.IntegerField(default=1)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='notes/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class QuestionPaper(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sem = models.IntegerField(default=1)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='question_papers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    