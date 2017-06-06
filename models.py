from google.appengine.ext import ndb

class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Game(ndb.Model):
    #user = ndb.ReferenceProperty(Account)
    numberPlayers = ndb.IntegerProperty()
    entryFee = ndb.FloatProperty()
    usersSignedUp = ndb.JsonProperty()
    #PrizeStructure (Model w/ variety of types)
    #StartTime
    #Duration
    #EndTime
    #GameResultKey (ForeignKey) - 1 to 1

class UserGames(ndb.Model):
    #userKey (Foreign Key) - 1 to 1
    gameKey = ndb.KeyProperty(Game, repeated=True)

class Account(ndb.Model):
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    userGames = ndb.KeyProperty(kind=UserGames)
    # phone =
    # Street Address
    # City
    # State
    # Zip
    # Date Joined
    # Last Login
    # UserBalanceKey (Foreign Key) - 1 to 1
