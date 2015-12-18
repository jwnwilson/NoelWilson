from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import signals
from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error

from noelwilson.apps.blog.models import Entry, Comment, Category, Tag
from noelwilson.apps.blog.forms import BlogForm, BlogManagerForm, CommentForm, \
										CategoryForm,CategoryManagerForm
from noelwilson.apps.main.views import getDataFile

import copy

def getBlogArchive():
	""" get years and months for archive
	  	Create dict with structure {year:{
										month:{
												[EntryData:{},
												 EntryData:{}]
											},
										month{
												[EntryData:{}]
											},
									year:{
										month{
												[EntryData:{}]
											}
										}
								}"""
	values = Entry.objects.values('created','id','title')
	dataDict = {}
	years = {}
	for value in values[::-1]:
		date = value['created']
		dataDict['date']= value['created']
		dataDict['id']=value['id']
		dataDict['title']= value['title']
		if not years.has_key(date.year):
			years[date.year] = {}
		if not years[date.year].has_key(date.strftime("%B")):
			years[date.year][date.strftime("%B")] = []
		years[date.year][date.strftime("%B")].append(copy.deepcopy(dataDict))
		
	return years
	
def getCategories():
	""" 
	get categories of posts
	"""
	categories = Category.objects.all().order_by('created')
	categoryList = []
	dataDict = {}
	for category in categories:
		date = category.created
		dataDict['date']= category.created
		dataDict['category_name'] = category.category_name
		dataDict['entries'] = Entry.objects.filter(category__category_name__contains = category.category_name)
		categoryList.append(copy.deepcopy(dataDict))
		
	return categoryList

@login_required
def blogEntry(request,blog_id= None):
	# New entry find unused pk
	pk = 1
	count = 1
	if blog_id == None:
		objs = Entry.objects.all()
		pk = (len(objs) + 1)
	else:
		pk= blog_id
	ctx = {}
	if request.method == "POST":
		blog_form = BlogForm(request.POST)
		if blog_form.is_valid():
			success = True
			title = blog_form.cleaned_data['title']
			text = blog_form.cleaned_data['text']
			tags = blog_form.cleaned_data['tags']
			category = blog_form.cleaned_data['category']
			
			#signals.message_sent.send(sender=BlogForm, title=ctx['title'])
			# Process tags
			if tags:
				# just deal with one tag for now
				firstTag = tags.split()[0]
				tag = Tag.objects.getOrCreateTag(firstTag)
			else:
				tag = Tag.objects.getOrCreateTag("None")
			# process categories
			if category:
				category = Category.objects.getOrCreateCategory(category)
			else:
				category = Category.objects.getOrCreateCategory("None")
			if blog_id:
				blogEntry = Entry.objects.get(pk= pk)
				blogEntry.text = text
				blogEntry.title = title
				blogEntry.tag = tag
				blogEntry.category = category
				blogEntry.save()
			else:
				blogEntry = Entry.objects.create(pk = pk,text = text,title = title,\
									user = request.user.get_profile(),tag = tag, \
									category = category)
				blogEntry.save()
			return redirect(reverse("blog_myBlog"))
		else:
			raise Exception("blog form not valid")
	else:
		if blog_id:
			blogEntry = Entry.objects.get(pk= pk)
			blog_form = BlogForm(initial={'title': blogEntry.title, 'text': blogEntry.text,
										'tags':"None"})
		else:
			blog_form = BlogForm(initial={'tags':"None"})
	ctx['blog_form'] = blog_form
	return render_to_response('blogEntry.html', ctx , context_instance= RequestContext(request))
	
def myBlog(request):
	entries = Entry.objects.published_entries()
	paginator = Paginator(entries, 5)
	# get page number from url ?page=#
	page_num = request.GET.get('page',1)
	try:
		page = paginator.page(page_num)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		page = paginator.page(1)
	# get about me text
	aboutMe = getDataFile("aboutMe.html")
	# get blog archive
	years = getBlogArchive()
	# get categories
	categories = getCategories()
	ctx = { 'page': page,
			'newID':1,
			'aboutMe':aboutMe,
			'years':years,
			'categories':categories,
	}
	return render_to_response('myblog.html', ctx , context_instance= RequestContext(request) )
	
@login_required
def blogManager(request):
	ctx = {}
	if request.method == "POST":
		if request.POST.get('blogManagerSubmit'):
			submitType = request.POST.get('blogManagerSubmit')
			# manage blogs
			blog_form = BlogManagerForm(request.user,request.POST)
			if blog_form.is_valid():
				submitType = request.POST.get('blogManagerSubmit')
				if submitType == 'delete_selected':
					# get selected entries
					selectedEntries = blog_form.clean_entryList(submitType)
					# delete from database
					for entry in selectedEntries:
						#Entry.objects.filter(published=True)
						obj = Entry.objects.filter(title= entry)
						obj.delete()
					# return to database manager
					return redirect(reverse("blog_blogManager"))
				elif submitType == 'edit_selected':
					existingEntry=None
					# get user entries
					entries = Entry.objects.getUser_entries(request.user)
					# find entry with matching title
					selectedEntryTitle = blog_form.clean_entryList(submitType)
					# get entry from database to populate default blog data
					for entry in entries:
						if entry and selectedEntryTitle:
							if entry.title == selectedEntryTitle[0]:
								existingEntry = entry
					# redirect to blog post
					return redirect(reverse("blog_blogEntry", args=(existingEntry.pk, )))
		elif request.POST.get('categoryManagerSubmit'):
			submitType = request.POST.get('categoryManagerSubmit')
			# manage blogs
			form = CategoryManagerForm(request.user,request.POST)
			if form.is_valid():
				submitType = request.POST.get('categoryManagerSubmit')
				if submitType == 'delete_selected':
					# get selected entries
					selectedCategories = form.clean_categoryList(submitType)
					# delete from database
					for category in selectedCategories:
						obj = Category.objects.filter(category_name= category)
						obj.delete()
					# return to database manager
					return redirect(reverse("blog_blogManager"))
				elif submitType == 'edit_selected':
					existingCategory=None
					# get user entries
					categories = Category.objects.published_entries()
					# find entry with matching title
					selectedCategories = form.clean_categoryList(submitType)
					# get entry from database to populate default blog data
					for category in categories:
						if category and selectedCategories:
							if category.category_name == selectedCategories[0]:
								existingCategory = category
					# redirect to blog post
					return redirect(reverse("blog_newCategory", args=(existingCategory.pk, )))
		else:
			raise server_error
			
	blog_form = BlogManagerForm(request.user)
	category_form = CategoryManagerForm(request.user)
	ctx = { 'blog_form': blog_form,
			'category_form':category_form,}
	return render_to_response('blogManager.html', ctx , context_instance= RequestContext(request) )

def postView(request, blog_id= None):
	if request.method == "POST":
		if blog_id == None:
			raise Exception("blog_id not found for comment")
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			text = comment_form.cleaned_data['text']
			author = comment_form.cleaned_data['author']
			if author == None:
				author = "anonymous"
			#signals.message_sent.send(sender=CommentForm, title=ctx['name'])
			comment = Comment.objects.create(text = text,author = author, entry = Entry.objects.get(id=blog_id))
			comment.save()
			return redirect(reverse("blog_PostView", args=(blog_id, ) ) )
		else:
			raise Exception("blog form not valid")
			
	# if blog_id == None get lasest id
	if blog_id == None:
		latestEntry = Entry.objects.all().order_by('created')[0]
		blog_id = latestEntry.id
	# get blog post blog_id == page_num
	entries = Entry.objects.published_entries()
	paginator = Paginator(entries, 1)
	# get page number from url ?page=#
	page_num = request.GET.get('page', blog_id)
	try:
		page = paginator.page(page_num)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		page = paginator.page(1)
	# get about me text
	aboutMe = getDataFile("aboutMe.html")
	# load comments
	comments = Comment.objects.filter(entry__id__contains=blog_id)
	# comment form
	comment_form = CommentForm(initial={'name':'Anonymous'})
	# get blog archive
	years = getBlogArchive()
	ctx = { 'comment_form': comment_form,
			'page': page,
			'aboutMe':aboutMe,
			'years':years,
			'comments':comments,
	}
	return render_to_response('postView.html', ctx , context_instance= RequestContext(request) )				

def newCategory(request, category_id= None):
	# New entry find unused pk
	pk = 1
	count = 1
	if category_id == None:
		objs = Category.objects.all()
		pk = (len(objs) + 1)
	else:
		pk= category_id
	
	if request.method == "POST":
		categoryForm = CategoryForm(request.POST)
		if categoryForm.is_valid():
			#categoryName = categoryForm.clean_category()
			categoryName = categoryForm.cleaned_data['category_name']
			success = True
			#signals.message_sent.send(sender=categoryForm, title=ctx['category_name'])
			if category_id:
				category = Category.objects.get(pk= pk)
				category.category_name =categoryName
				category.save()
			else:
				category = Category.objects.create(pk= pk, category_name= categoryName)
				category.save()
			return redirect(reverse("blog_blogManager"))
		else:
			raise Exception("category form not valid")
			
	# if this category exists get data else create blank form
	if category_id:
		category = Category.objects.get(pk= pk)
		categoryForm = CategoryForm(initial={'category_name': category.category_name})
	else:
		categoryForm = CategoryForm(initial={'category_name':'None'})
	# get about me text
	aboutMe = getDataFile("aboutMe.html")
	# get blog archive
	years = getBlogArchive()
	ctx= { 	'categoryForm': categoryForm,
			'aboutMe':aboutMe,
			'years':years,
	}
	return render_to_response('newCategory.html', ctx , context_instance= RequestContext(request))
	
def archive(request, month = None):
	base_qs = Entry.objects.published_entries()
	in_archive_count = base_qs.count()
	page = None
	
	if month == None:
		month = backend.DatabaseOperations(connections).date_trunc_sql('month','created')
		per_month_count = base_qs.extra({'date':month}).values('date').annotate(count=Count('pk')).order_by('date')
		month = ''
		year = ''
	else:
		per_month_count = []
		today = datetime.datetime.today()
		year = today.year
		entries = base_qs.filter(created__year=today.year,created__month=today.month)
		paginator = Paginator(entries, 5)
	
		# get page number from url ?page=#
		page_num = request.GET.get('page',1)
		try:
			page = paginator.page(page_num)
		except EmptyPage:
			page = paginator.page(paginator.num_pages)
		except PageNotAnInteger:
			page = paginator.page(1)
	
	ctx = {'page': page,
		'month':month,
		'year':year,
		"in_archive_count": in_archive_count,
		"per_month_count": per_month_count,
	}
	return render_to_response('archive.html', ctx, context_instance= RequestContext(request))
	

