from google.cloud import ndb


class Book(ndb.Model):
	isbn = ndb.IntegerProperty()
	name = ndb.StringProperty()
	author = ndb.StringProperty()


class Member(ndb.Model):
	name = ndb.StringProperty()


class Borrow(ndb.Model):
	book_id = ndb.IntegerProperty()
	member_id = ndb.StringProperty()
	returned = ndb.BooleanProperty(default=False)
