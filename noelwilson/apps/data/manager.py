from django.db import models

class ProjectManager(models.Manager):
	def published_projects(self):
		return self.model.objects.filter(published=True).order_by('-updated')
		
