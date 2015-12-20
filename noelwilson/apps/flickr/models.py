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
            
def sync_flickr_photos(*args, **kwargs):
    API_KEY = '12e6b819f6ab42886c7a3ba4d21399e7'
    USER_ID = '83155946@N06'
    FLICKR_SECRET = 'bce69eacaf008f50'
    
    photoSet = ''
    cur_page = 1            # Start on the first page of the stream
    paginate_by = 5         # Get 20 photos at a time
    dupe = False            # Set our dupe flag for the following loop
    
    if kwargs.has_key('album') == False:
        raise Exception('Expected kwarg \'name\' not found when calling: %s' % (sys._getframe(1).f_code.co_name))
    
    # if last sync less than hour return
    if kwargs['album'] == '3DArtwork':
        last_sync = cache.get('last_sync3D')
        if last_sync:
            return
    elif kwargs['album'] == '2DArtwork':
        last_sync = cache.get('last_sync2D')
        if last_sync:
            return
    # get correct set
    try:
        currentAlbum = Album.objects.get(name= kwargs['album'])
    except ObjectDoesNotExist:
        raise Exception('Album not found with name %s' % (kwargs['album']))

    flickr = flickrapi.FlickrAPI(API_KEY, FLICKR_SECRET, cache=False, store_token=False)    # Get our flickr client running
    #flickr.cache = cache

    while (not dupe):
        photos = flickr.walk_set(currentAlbum.flickr_id,per_page=paginate_by)
        
        for photo in photos:
            try:
                row = Photo.objects.get(flickr_id=photo.get("id"), flickr_secret=str(photo.get("secret")))
                row.last_sync = now()
                row.save()
                
                # Raise exception if photo doesn't exist in our DB yet
                # If the row exists already, set the dupe flag
                dupe = True
            except ObjectDoesNotExist:
                p = Photo(
                title = str(photo.get("title")),
                flickr_id = int(photo.get("id")),
                flickr_owner = str(photo.get("owner")),
                flickr_server = int(photo.get("server")),
                flickr_secret = str(photo.get("secret")),
                album = currentAlbum,
                last_sync = now(),
                )
                p.save()

                if (dupe):   # If we hit a dupe or if we did the last page...
                        break
            else:
                cur_page += 1
        # set cache value to avoid unnecessary syncing
        cache.set('last_sync',now(),30)
