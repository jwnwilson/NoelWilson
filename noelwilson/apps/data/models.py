from django.db import models
from django.db.models.signals import post_save
from noelwilson.apps.data import handlers
from noelwilson.apps.data.manager import ProjectManager

class ProjectLists(models.Model):
    projectName = models.TextField()
    
    def __unicode__(self):
        return self.projectName

class Project(models.Model):
    projectList = models.ForeignKey(ProjectLists)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length= 64)
    text = models.TextField()
    videoFile = models.CharField(max_length= 200)
    imageFile = models.CharField(max_length= 200)
    objects = ProjectManager()
    
    def __unicode__(self):
        return u"%s - %s" % (self.title,self.created)

post_save.connect(handlers.model_saved, sender=Project)
