from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('noelwilson.apps.accounts.views',
    url(r'^profile/$', 'profile', name="accounts_profile"),
)

urlpatterns += patterns('',
	url(r'^login/$', login , kwargs= {'template_name':'login.html'}, name= "accounts_login"),
	url(r'^logout/$', logout , kwargs = {'next_page':"/"}, name= "accounts_logout"),
)
