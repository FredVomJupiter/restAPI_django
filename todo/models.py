import django
from django.conf import settings
from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.id}) {self.title}'