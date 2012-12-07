# -*- coding: utf-8 -*-

import os, datetime
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort

# import all of mongoengine
from mongoengine import *

# import data models
import models

app = Flask(__name__)   # create our flask app

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
connect('mydata', host=os.environ.get('MONGOLAB_URI'))
print "Connecting to MongoLabs"


# categories = ['web','physical computing','software','video','music','installation','assistive technology','developing nations','business','social networks']

# --------- Routes ----------

# this is our main page
@app.route("/")
def index():

	templateData = {
		'projects' : models.Project.objects(),
	}
	return render_template("main.html", **templateData)

@app.route("/projects/add", methods=["POST"])
def newproject():
	
	app.logger.debug('project form response data')
	app.logger.debug(request.form)
	# app.logger.debug('list of submitted categories')
	# app.logger.debug(request.form.getlist('categories'))

	# get form data - create new idea
	project = models.Project()  #JB - inside of the models.py object, we're going to get the class Idea
	project.user = request.form.get('user','Anonymous')
	project.title = request.form.get('title','No Title')
	project.slug = slugify(project.title + " " + project.user)
	# idea.idea = request.form.get('idea','')
	# idea.categories = request.form.getlist('categories')
	
	project.save()

	return redirect('/projects/%s' % project.slug)

@app.route("/projects/<project_slug>") #JB - this slug can be named anything...it's just for our use
def project_display(project_slug):

	## JB - You could, e.g., @app.route("/ideas/<idea_slug>/<color>/<shape>/")
	## def idea_display(idea_slug, color, shape):

	# get idea by idea_slug
	try:
		project = models.Project.objects.get(slug=project_slug)
	except:
		abort(404)

	# prepare template data
	templateData = {
		'project' : project
	}

	# render and return the template
	return render_template('project.html', **templateData)

# slugify the title 
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

## -------------- PREVIOUS ROUTES --------------------

# @app.route("/category/<cat_name>")
# def by_category(cat_name):

# 	try:
# 		ideas = models.Idea.objects(categories=cat_name)
# 	except:
# 		abort(404)

# 	templateData = {
# 		'current_category' : {
# 			'slug' : cat_name,
# 			'name' : cat_name.replace('_',' ')
# 		},
# 		'ideas' : ideas,
# 		'categories' : categories
# 	}

# 	return render_template('category_listing.html', **templateData)

# @app.route("/ideas/add", methods=["POST"])
# def newidea():
	
# 	app.logger.debug('idea form response data')
# 	app.logger.debug(request.form)
# 	app.logger.debug('list of submitted categories')
# 	app.logger.debug(request.form.getlist('categories'))

# 	# get form data - create new idea
# 	idea = models.Idea()  #JB - inside of the models.py object, we're going to get the class Idea
# 	idea.creator = request.form.get('creator','anonymous')
# 	idea.title = request.form.get('title','no title')
# 	idea.slug = slugify(idea.title + " " + idea.creator)
# 	idea.idea = request.form.get('idea','')
# 	idea.categories = request.form.getlist('categories')
	
# 	idea.save()

# 	return redirect('/ideas/%s' % idea.slug)

# @app.route("/ideas/<idea_slug>") #JB - this slug can be named anything...it's just for our use
# def idea_display(idea_slug):

# 	## JB - You could, e.g., @app.route("/ideas/<idea_slug>/<color>/<shape>/")
# 	## def idea_display(idea_slug, color, shape):

# 	# get idea by idea_slug
# 	try:
# 		idea = models.Idea.objects.get(slug=idea_slug)
# 	except:
# 		abort(404)

# 	# prepare template data
# 	templateData = {
# 		'idea' : idea
# 	}

# 	# render and return the template
# 	return render_template('idea_entry.html', **templateData)
	
# @app.route("/ideas/<idea_id>/comment", methods=['POST'])
# def idea_comment(idea_id):

# 	name = request.form.get('name')
# 	comment = request.form.get('comment')

# 	if name == '' or comment == '':
# 		# no name or comment, return to page (JB - this page)
# 		return redirect(request.referrer)


# 	#get the idea by id
# 	try:
# 		idea = models.Idea.objects.get(id=idea_id)
# 	except:
# 		# error, return to where you came from
# 		return redirect(request.referrer)


# 	# create comment
# 	comment = models.Comment()
# 	comment.name = request.form.get('name')
# 	comment.comment = request.form.get('comment')
	
# 	# append comment to idea
# 	idea.comments.append(comment)
# 	idea.save()

# 	return redirect('/ideas/%s' % idea.slug)


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404


# # slugify the title 
# # via http://flask.pocoo.org/snippets/5/
# _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
# def slugify(text, delim=u'-'):
# 	"""Generates an ASCII-only slug."""
# 	result = []
# 	for word in _punct_re.split(text.lower()):
# 		result.extend(unidecode(word).split())
# 	return unicode(delim.join(result))


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	