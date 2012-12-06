# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime

class Log(Document):
	text = StringField()
	timestamp = DateTimeField(default=datetime.now()) 

class Comment(EmbeddedDocument): #something you put inside another doc (you never use .save on this)
	name = StringField()
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())

class Idea(Document):

	creator = StringField(max_length=120, required=True)
	title = StringField(max_length=120, required=True)
	slug = StringField()
	idea = StringField(required=True)

	# Category is a list of Strings
	categories = ListField(StringField(max_length=30))

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())
	

