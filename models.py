# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime

# class Log(Document):
# 	text = StringField()
# 	timestamp = DateTimeField(default=datetime.now()) 

# class Comment(EmbeddedDocument): #something you put inside another doc (you never use .save on this)
# 	name = StringField()
# 	comment = StringField()
# 	timestamp = DateTimeField(default=datetime.now())

# class Idea(Document):

# 	creator = StringField(max_length=120, required=True)
# 	title = StringField(max_length=120, required=True)
# 	slug = StringField()
# 	idea = StringField(required=True)

# 	# Category is a list of Strings
# 	categories = ListField(StringField(max_length=30))

# 	# Comments is a list of Document type 'Comments' defined above
# 	comments = ListField( EmbeddedDocumentField(Comment) )

# 	# Timestamp will record the date and time idea was created.
# 	timestamp = DateTimeField(default=datetime.now())
	
class User(Document):
	name = StringField()
	total_paid = FloatField()
	# email = EmailField()
	# password = StringField()


# class Purchase(EmbeddedDocument):
class Purchase(Document):

	user = StringField()
	dollar_amount = DecimalField()
	description = StringField()
	date = DateTimeField(default=datetime.now())
	quantity = IntField()
	# url = URLField()


class Project(Document):
	title = StringField()
	purchase = ListField(ReferenceField(Purchase)) #use .append 
	# purchase = ListField(EmbeddedDocumentField(Purchase)) #use .append 
	user = ListField(ReferenceField(User)) #ReferenceField
	slug = StringField()
	total_cost = FloatField()
	cost_per_user = FloatField()
	# start_date = DateTimeField(default=datetime.now())
	# end_date = DateTimeField()
	# course = StringField()  # the ITP class the project was assigned for
	# password = StringField(default=Project.name)
