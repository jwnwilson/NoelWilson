NoelWilson
==========

My first retired website build with Django, updated to work on Google App Engine

https://jwnwilson-eu.appspot.com/

Written in python 2 I find this project nostalgic to look at.

# Deployment

Updated and deployed to cloud run to test it out:

gcloud builds submit --tag gcr.io/jwnwilson-eu/noel-wilson
gcloud run deploy --image gcr.io/jwnwilson-eu/noel-wilson --platform managed