from google.cloud import ndb


class Book(ndb.Model):
	isbn = ndb.IntegerProperty()
	name = ndb.StringProperty()
	author = ndb.StringProperty()
	taken = ndb.BooleanProperty(default=False)
	taken_by = ndb.KeyProperty()

	def get_dict(self):
		data = {**self.to_dict(), **{'id':self.key.id()}}
		if 'taken_by' in data and data['taken_by'] is not None:
			data['taken_by'] = data['taken_by'].id()
		return data


class Member(ndb.Model):
	name = ndb.StringProperty()

	def get_dict(self):
		return {**self.to_dict(), **{'id':self.key.id()}}


class User(ndb.Model):
	name = ndb.StringProperty()
	password = ndb.StringProperty()
	member_id = ndb.KeyProperty()

	def get_dict(self):
		data = {**self.to_dict(), **{'id':self.key.id(), 'email':self.key.id()}}
		if 'member_id' in data and data['member_id'] is not None:
			data['member_id'] = data['member_id'].id()
		return data
