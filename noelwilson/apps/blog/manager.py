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

class CategoryManager(models.Manager):
	def published_entries(self):
		return self.model.objects.all().order_by('-created')
		
	def getOrCreateCategory(self, categoryName):
		if self.model.objects.filter(category_name__contains=categoryName):
			return self.model.objects.filter(category_name__contains=categoryName)[0]
		else:
			category = self.model.objects.create(category_name= categoryName)
			category.save()
			return category
class TagManager(models.Manager):
	def getOrCreateTag(self, tagName):
		if self.model.objects.filter(tag_name__contains=tagName):
			return self.model.objects.filter(tag_name__contains=tagName)[0]
		else:
			tag = self.model.objects.create(tag_name= tagName)
			tag.save()
			return tag
