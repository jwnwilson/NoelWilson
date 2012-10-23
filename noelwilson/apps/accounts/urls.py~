from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('blogV2.apps.accounts.views',
    url(r'^profile/$', 'profile', name="accounts_profile"),
    url(r'^register/$', 'register', name="accounts_register"),
    url(r'^myBlog/$', 'myBlog', name="accounts_myBlog"),
    url(r'^myBlog/blogEntry/(?P<blog_id>\d+)/$', 'blogEntry', name="accounts_blogEntry"),
    url(r'^myBlog/blogEntry/', 'blogEntry', name="accounts_blogEntryDefault"),
    url(r'^myBlog/blogManager/$', 'blogManager', name="accounts_blogManager"),
)

urlpatterns += patterns('',
	url(r'^login/$', login , kwargs= {'template_name':'login.html'}, name= "accounts_login"),
	url(r'^logout/$', logout , kwargs = {'next_page':"/"}, name= "accounts_logout"),
)
