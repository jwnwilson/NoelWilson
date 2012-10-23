from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('noelwilson.apps.blog.views',
    url(r'^myBlog/$', 'myBlog', name="blog_myBlog"),
    url(r'^myBlog/blogEntry/(?P<blog_id>\d+)/$', 'blogEntry', name="blog_blogEntry"),
    url(r'^myBlog/blogEntry/', 'blogEntry', name="blog_blogEntryDefault"),
    url(r'^myBlog/blogManager/$', 'blogManager', name="blog_blogManager"),
    url(r'^myBlog/postView/(?P<blog_id>\d+)/$', 'postView', name="blog_PostView"),
    url(r'^myBlog/postView/$', 'postView', name="blog_PostViewDefault"),
    url(r'^myBlog/newCategory/$', 'newCategory', name="blog_newCategory"),
)
