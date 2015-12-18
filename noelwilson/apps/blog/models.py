from django.db import models
from django.db.models.signals import post_save
from noelwilson.apps.data import handlers
from noelwilson.apps.accounts.models import UserProfile
from noelwilson.apps.blog.manager import EntryManager, CategoryManager,TagManager

class Tag(models.Model):
	tag_name = models.CharField(max_length= 64)
	created = models.DateTimeField(auto_now_add=True)
	
	objects = TagManager()
	#entry = models.ForeignKey(Entry)
	def __unicode__(self):
		return u"%s" % (self.tag_name)
class Category(models.Model):
	category_name = models.CharField(max_length= 64)
	created = models.DateTimeField(auto_now_add=True)
	#entry = models.ForeignKey(Entry)
	objects = CategoryManager()
	def __unicode__(self):
		return u"%s" % (self.category_name)

class Entry(models.Model):
	user = models.ForeignKey(UserProfile)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length= 64)
	text = models.TextField()
	published = models.BooleanField(db_index=True, default= True)
	objects = EntryManager()
	tag = models.ForeignKey(Tag)
	category =  models.ForeignKey(Category)
	
	def __unicode__(self):
		return u"%s - %s" % (self.title,self.created)

post_save.connect(handlers.model_saved, sender=Entry)
	
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60)
    text = models.TextField()
    entry = models.ForeignKey(Entry)

    def __unicode__(self):
        return unicode("%s: %s" % (self.entry, self.text[:60]))
