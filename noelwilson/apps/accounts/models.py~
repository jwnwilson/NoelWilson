from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	email =  models.CharField(max_length=100)
	updated = models.DateTimeField(auto_now=True)
