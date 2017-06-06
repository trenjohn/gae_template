#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START imports]
from models import *
from tasks import *
import os
import urllib
import logging
import json

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START guestbook]
class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]

class AccountPage(webapp2.RequestHandler):

    def get(self):
        a = Account()
        a.firstName ='Trent'
        a.lastName='Johnson'
        a.email='trent.matt.j@gmail.com'

        g1 = Game()
        g1.numberPlayers = 10
        g1.entryFee = 5.00

        g2 = Game()
        g2.numberPlayers = 6
        g2.entryFee = 10.00

        g1result = g1.put()
        g2result = g2.put()

        myusergames = UserGames(gameKey = [g1result,g2result])
        myusergamesresult = myusergames.put()

        a.userGames = myusergamesresult

        result = a.put()

        acc = result.get()
        usergamelist = acc.userGames
        u = usergamelist.get()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(acc) #writes user object
        self.response.write('\n\n')
        self.response.write(acc.userGames) #writes
        self.response.write('\n\n')
        self.response.write(u)
        self.response.write('\n\n')
        for game in u.gameKey:
            blah = game.get()
            self.response.write(blah)

        #for game in u:
        #    self.response.write(game.get())

class Lobby(webapp2.RequestHandler):

    def get(self):
        g  = Game.query(Game.numberPlayers == 1)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'games': g,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('lobby.html')
        self.response.write(template.render(template_values))
        # self.response.headers['Content-Type'] = 'text/plain'
        # for game in g:
        #     self.response.write(game)

class About(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('About Us')

class Contact(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('contact.html')
        self.response.write(template.render)

class FAQ(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('FAQ')

class CreateGames(webapp2.RequestHandler):

    def get(self):

        al = Game.query(Game.numberPlayers == 1)

        while al.count(limit=None) < 10:
            gspot = Game()
            gspot.numberPlayers = 1
            gspot.entryFee = 5.00
            gspot.usersSignedUp = 0
            result = gspot.put()

class GamePage(webapp2.RequestHandler):

    def get(self, url):

        url = self.request.url
        gameID = os.path.basename(os.path.normpath(url))
        gameID = int(gameID)
        game = Game()
        game = game.get_by_id(gameID)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'game': game,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('gamepage.html')
        self.response.write(template.render(template_values))

    def post(self, url):

        url = self.request.url
        gameID = os.path.basename(os.path.normpath(url))
        gameID = int(gameID)
        game = Game()
        game = game.get_by_id(gameID)

        #data = json.loads({'users': [{'1':'trenjohn'}]})

        current = game.usersSignedUp
        new = current + 1

        game.usersSignedUp = new

        result = game.put()

        #query_params = {'game': gameID}
        self.redirect(url)

class SignedUp(webapp2.RequestHandler):

    def get(self, url):

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('You are signed up!')

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/about', About),
    ('/contact', Contact),
    ('/faq', FAQ),
    ('/account', AccountPage),
    ('/tasks/create_games', CreateGames),
    ('/lobby', Lobby),
    ('/g/(.*)', GamePage),
    ('/e/(.*)', SignedUp),
], debug=True)
# [END app]
