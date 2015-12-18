from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from noelwilson import settings
from noelwilson.apps.data.models import Project, ProjectLists
from noelwilson.apps.flickr.models import Photo, sync_flickr_photos
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files import File 

import os, sys
import datetime

def getDataFile(fileName):
	# get intro text
	filePath = (settings.STATIC_ROOT + "/data/" + fileName)
	if os.path.isfile(filePath):
		File = open(filePath)
		introText = File.read()
		File.close()
	else:
		introText = ''
	return introText

def homepage(request):		
	# get intro text
	introText = getDataFile("introText.html")
	ctx = { 'introText':introText}
	return render_to_response('home.html', ctx , context_instance= RequestContext(request) )
	
def technical(request, projectName=None):
	projects = []
	if projectName == None:
		projectName = "webDev"
	# get contact info
	contactInfo = getDataFile("contactInfo.html")
	# get projects	
	projects = Project.objects.filter(projectList__projectName__contains= projectName )
	for project in projects:
		project.text = getDataFile(project.text)
		project.videoFile = getDataFile(project.videoFile)
	ctx = { 'projects':projects,
			'contactInfo':contactInfo}
	return render_to_response('technical.html', ctx , context_instance= RequestContext(request) )
	
def artwork(request, projectName=None):
	projects = []
	if projectName == None:
		projectName = "3DArtwork"
	# get contact info
	# contactInfo = getDataFile("contactInfo.html")
	# get projects	
	projects = Project.objects.filter(projectList__projectName__contains= projectName )
	for project in projects:
		project.text = getDataFile(project.text)
		project.videoFile = getDataFile(project.videoFile)
	# get most recent artwork pictures
	sync_flickr_photos(album = projectName)
	photos = Photo.objects.filter(album__name__contains= projectName )
	# Seperate artwork up into pages of 9 entries
	paginator = Paginator(photos, 9)
	# get page number from url ?page=#
	page_num = request.GET.get('page',1)
	try:
		page = paginator.page(page_num)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		page = paginator.page(1)
	
	# get gallery type
	if projectName == "2DArtwork":
		galleryType = '2D'
	else:
		galleryType = '3D'
	ctx = { 'projects':projects,
			'photos':page,
			'galleryType': galleryType,}
	return render_to_response('artwork.html', ctx , context_instance= RequestContext(request) )
	
def training(request, projectName=None):
	projects = []
	if projectName == None:
		projectName = "training"
	# get projects	
	projects = Project.objects.filter(projectList__projectName__contains= projectName )
	for project in projects:
		project.text = getDataFile(project.text)
		project.videoFile = getDataFile(project.videoFile)
	ctx = { 'projects':projects}
	return render_to_response('training.html', ctx , context_instance= RequestContext(request) )
	
def download(request, filePath=None):
	"""
	This function is not used as of yet still looking for a good down load
	handling method
	"""
	if filePath == None:
		raise Exception("File not found for download.")
	downloadFile  = open(filePath, "r")
	django_file = File(downloadFile)
	
	raise Http404

