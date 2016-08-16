#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#XBully
#Team Ellis
#By Peirce Chow Zheng Jie, Koh Yi Ting and Ng Teng Guan Gary
#July 2016

import webapp2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import cgi
import time

import sys
sys.path.insert(0, 'libs')

import aiml 


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
autoescape=True)

users_arr = []
bots = []
triggers=["die","dying","suicide","suicidal","kill","killing"]

class User():
    def __init__(self,name,position):
        self.name = name
        self.number = position
	
def position(name):
    position = 0
    for user in users_arr:
        if user.name == name:
            return position
        position += 1
    #if nothing is returned means nth is found, so function below is evoked

    u = User(name,position) 
    users_arr.append(u)


    b = aiml.Kernel()
    b.learn("std-startup.xml")
    b.respond("load aiml b")
    bots.append(b)

    return position      
	
def respond(name,resp):
    return (bots[position(name)].respond(resp)) #because each user_obj is mapped to each bot obj with the same index
	
class Name(ndb.Model):
	name= ndb.StringProperty(indexed= True)
	datetime = ndb.DateTimeProperty(auto_now_add=True) #gets the current date and time
	
def name():
	return ndb.Key("User", 3)
	
# class Incoming(ndb.Model): 						# User input
	# name = ndb.StringProperty(indexed=True)
	# message = ndb.StringProperty(indexed= True)
	# datetime = ndb.DateTimeProperty(auto_now_add=True)#gets the current date and time
	# human = ndb.StringProperty(indexed=False)	#not really important, just for JINJA2 to distinguise betweeen human and bot
	
# def incoming_key():
	# return ndb.Key("Input", 3)
	
# class Outgoing(ndb.Model):						#Bot response
	# name = ndb.StringProperty(indexed=True)
	# message = ndb.StringProperty(indexed= True)
	# datetime = ndb.DateTimeProperty(auto_now_add=True)#gets the current date and time
	# bot = ndb.StringProperty(indexed=False)													
	
# def outgoing_key():
	# return ndb.Key("Output", 3)

class Log(ndb.Model): 						# User input
	name = ndb.StringProperty(indexed=True) 			#from who
	message = ndb.StringProperty(indexed= True)
	datetime = ndb.DateTimeProperty(auto_now_add=True)	#gets the current date and time
	human = ndb.BooleanProperty(indexed=True)			#not really important, just for JINJA2 to distinguise betweeen human and bot			

class GetResponse(webapp2.RequestHandler): #this gets the response fron user input, which generates the bot's response
										   # and then stores both the user and the bot's response in the datastore
	def post(self):
		user_resp = self.request.get("user_input") #the form name is called user_input, so when i click on the send button it calls the GetResoponse class with a post method
		user=users.get_current_user()
		url = users.create_logout_url(self.request.uri)
		if user:
		#get user's incoming msg and stroes them in the datastore with their names
			if len(user_resp)>0:
				h = Log()             #incoming response from human
				h.message = user_resp
				h.name = user.nickname()
				h.human = True
				#i.put()
				
				#STARTING BOT RESPONSE
				#kernel = aiml.Kernel()
				#kernel.learn("std-startup.xml")
				#kernel.respond("load aiml b")
				#the above reading of files has been placed at the top
				bot_resp = respond(user.nickname(),user_resp)

				for trigger in triggers:
					if trigger in user_resp:
						bot_resp="I feel that your safety is being compromised, please speak to a counsellor"
					
				b = Log()
				b.message = bot_resp
				b.name = user.nickname()
				b.human = False
				
				h.put()
				b.put()
				
				time.sleep(1) #add some delay to demonstrate that the bot is "thinking"
							  #maybe we can randomise inthe future based on the length of the response
				if bot_resp=="I feel that your safety is being compromised, please speak to a counsellor":
					self.redirect('/call')
				else:
					self.redirect('/profile')
			
			else:
				self.redirect('/profile')
		
		else:
			self.redirect(users.create_login_url(self.request.uri))

				
				
class Bully(webapp2.RequestHandler):
	
	def get(self):
	
		user = users.get_current_user()
		url = users.create_logout_url(self.request.uri)
		if user:
			url = users.create_logout_url(self.request.uri)
		
		else:
			self.redirect('/')

	
		template_values = {'url':url
		}
		template = JINJA_ENVIRONMENT.get_template('templates/bully.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))

class Victim(webapp2.RequestHandler):
	
	def get(self):		

		user = users.get_current_user()
		url = users.create_logout_url(self.request.uri)
		if user:
			url = users.create_logout_url(self.request.uri)
		
		else:
			self.redirect('/')
			
		template_values = {'url':url
		}
		template = JINJA_ENVIRONMENT.get_template('templates/victim.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
		
		
class Quotes(webapp2.RequestHandler):
	
	def get(self):		
		user = users.get_current_user()
		url = users.create_logout_url(self.request.uri)
		if user:
			url = users.create_logout_url(self.request.uri)
		
		else:
			self.redirect('/')
			
		template_values = {
		'url':url
		}
		template = JINJA_ENVIRONMENT.get_template('templates/quotes.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
		
class Profile(webapp2.RequestHandler):
	
	def get(self):		
		user = users.get_current_user()
		objs=''
		bot_msg=''
		url = users.create_logout_url(self.request.uri)
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			try:
				objs=Log.query().order(Log.datetime).filter(Log.name==user.nickname()).fetch()
			except:
				pass
			try:		
				bot_msg = objs[-1].message
				del objs[-1]
			except:
				pass
			
			if bot_msg == '':						#When there is nothing from the datastore. Usually when I clear history OR new user
				bot_msg = "Hi, my name is Ellis :)"
				b = Log()
				b.message = bot_msg
				b.name = user.nickname()
				b.human = False
				b.put()
				
			if len(Name.query().filter(Name.name==user.nickname()).fetch()) == 0: #check whether the name exists in the database, if not then store it inside
			
				self.response.write(user.nickname())
				n = Name()
				n.name = user.nickname()
				n.put()
				
			# if bot_msg=="I feel that your safety is being compromised, please speak with our counsellor":
				# time.sleep(1)
				# self.redirect('/call')	
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'	
			self.redirect('/')	
		
		template_values = {
			"objs": objs,
			"bot_msg": bot_msg,
			"url":url,
			"url_linktext":url_linktext
		
		}
		template = JINJA_ENVIRONMENT.get_template('templates/profile.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))

class Call(webapp2.RequestHandler):
	
	def get(self):		
		user = users.get_current_user()
		url = users.create_logout_url(self.request.uri)
		if user:
			url = users.create_logout_url(self.request.uri)
		
		else:
			self.redirect('/')
			
		template_values = {
		'url':url
		}
		template = JINJA_ENVIRONMENT.get_template('templates/call.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
		
class MainHandler(webapp2.RequestHandler):
	
	def get(self):		
		url = users.create_login_url(self.request.uri)
		user = users.get_current_user()
		if user:
			self.redirect('/profile')
		template_values = {
		'url':url
		}
		template = JINJA_ENVIRONMENT.get_template('templates/login.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
				
app = webapp2.WSGIApplication([
	('/getresponse', GetResponse),
	('/bully', Bully),
	('/victim', Victim),
	('/quotes', Quotes),
	('/profile', Profile),
	('/call', Call),
	('/', MainHandler)
], debug=True)
