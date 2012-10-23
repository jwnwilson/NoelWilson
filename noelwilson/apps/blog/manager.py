from django.db import models

class EntryManager(models.Manager):
	def published_entries(self):
		return self.model.objects.filter(published=True).order_by('-updated')
	def getUser_entries(self,user):
		allObj = self.model.objects.all().order_by('-updated')
		retObj =[]
		for entry in allObj:
			if user == entry.user.user:
				retObj.append(entry)
		return retObj
