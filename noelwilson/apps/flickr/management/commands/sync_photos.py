from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.utils.timezone import now
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from noelwilson.apps.flickr.manager import PhotoManager
from noelwilson.apps.flickr.models import *

import flickrapi
import os, sys, platform
import inspect

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

class Command(BaseCommand):
    args = ''
    help = 'Syncs flickr photos'

    def handle(self, *args, **options):
        sync_flickr_photos(album="3DArtwork")
        sync_flickr_photos(album="2DArtwork")