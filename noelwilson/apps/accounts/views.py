from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import signals

from noelwilson.apps.blog.models import Entry
from noelwilson.apps.accounts.forms import RegisterForm

import re

@login_required
def profile(request):
	try:
		profile = request.user.get_profile()
		ctx = {'profile': profile,
		'title': str(profile.user).title(),
		'email':str(profile.user.email)}
	except KeyError: 
		return redirect(reverse("accounts_register"))
	return render_to_response('profile.html',ctx,context_instance= RequestContext(request))
	
def register(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save()
		user.backend = settings.AUTHENTICATION_BACKENDS[0]
		login(request, user)
		return redirect(reverse("accounts_profile"))
		
	ctx = {"form":form}
	return render_to_response("register.html",ctx, context_instance= RequestContext(request))


