#!/usr/bin/env python

# [START imports]
from models import *
from tasks import *
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

class CreateGames(webapp2.RequestHandler):

    def get(self):

        al = Game.query(Game.numberPlayers == 10)

        while len(al) < 100:
            g = Game()
            g.numberPlayers = 10
            g.entryFee = 5.00
            g.put()
