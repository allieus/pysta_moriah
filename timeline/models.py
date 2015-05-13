from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
	contents = models.TextField(null=False)
	image = models.TextField()
	owner = models.OneToOneField(settings.AUTH_USER_MODEL)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
