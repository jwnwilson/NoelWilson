from django.contrib import admin
from models import Tag, Category, Entry, Comment

admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Entry)