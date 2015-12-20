from django.db import models
from django.utils.timezone import now
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from noelwilson.apps.flickr.manager import PhotoManager

import flickrapi
import os, sys, platform
import inspect


class BigintField(models.IntegerField):
    def db_type(self,connection):
        return 'BIGINT(20)'


class Album(models.Model):
    flickr_id = BigintField(unique=True)
    name = models.CharField(blank=True, max_length=100)
    show = models.BooleanField(default=True)
    last_sync = models.DateTimeField(blank=True, null=True, editable=False)
    
    def __unicode__(self):
        return self.name

class Photo(models.Model):
    title = models.CharField(blank=True, max_length=100)
    flickr_id = BigintField()
    flickr_owner = models.CharField(max_length=20)
    flickr_server = models.IntegerField()
    flickr_secret = models.CharField(max_length=50)
    album = models.ForeignKey(Album, null=True, blank=True, default = None)
    created = models.DateTimeField(auto_now_add=True)
    last_sync = models.DateTimeField(blank=True, null=True, editable=False)
    objects = PhotoManager()
    
    class Admin:
        list_display = ('title',)
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return "/photos/%s/" % (self.id)
        
    def get_pic_url(self, size='small'):
        # small_square=75x75
        # thumb=100 on longest side
        # small=240 on longest side
        # medium=500 on longest side
        # large=1024 on longest side
        # original=duh
        
        base_url = "http://static.flickr.com"
        size_char='s'  # default to small_square
        
        if size == 'small_square':
                size_char='_s'
        elif size == 'thumb':
                size_char='_t'
        elif size == 'small':
                size_char='_m'
        elif size == 'medium':
                size_char=''
        elif size == 'large':
                size_char='_b'
        elif size == 'original':
                size_char='_o'
        
        return "%s/%s/%s_%s%s.jpg" % (base_url, self.flickr_server, self.flickr_id, self.flickr_secret, size_char)
