from google.cloud import ndb


client = ndb.Client()


# class Contact(ndb.Model):
#     name = ndb.StringProperty()
#     phone = ndb.StringProperty()
#     email = ndb.StringProperty()


# with client.context():
# 	ancestor_key = ndb.Key("ContactGroup", "work")
# 	contact1 = Contact(parent=ancestor_key,
#     	name="Jane Smith",
# 		phone="555 617 8993",
# 		email="jane.smith@gmail.com")
# 	contact1.put()
# 	# x = contact1.get()
# 	print(dir(contact1))
# 	print(contact1)
# 	print(contact1.key)
# 	print(contact1.key.id(), contact1.key.integer_id())
# 	print(dir(contact1.key))
# 	print(contact1.to_dict())
	# print(x)
	# print(contact1 == x)
	# contact2 = Contact(parent=ancestor_key,
	# 	name="Jane Doe",
	# 	phone="555 445 1937",
	# 	email="jane.doe@gmail.com")
	# contact2.put()

# with client.context():
# 	ancestor_key = ndb.Key("Contact", 5632499082330112)
# 	query = Contact.query(ancestor=ancestor_key)
# 	print(query.count())
# 	for i in query:
# 		print(i)
	# query = Contact.query().filter(Contact.name == "John Smith")
	# print(query)
	# # print(type(query))
	# for i in query:
	# 	# print(type(i))
	# 	print(i.phone)

# with client.context():
# 	ancestor_key = ndb.Key("ContactGroup", "work")
# 	query = Contact.query(ancestor=ancestor_key)
# 	# for i in query:
# 	# 	print(i)
# 	# query = Contact.query(ancestor=ndb.Key('ContactGroup', 'work', 'Contact', 6205318602162176))
# 	print(query)
# 	print(dir(query))
# 	print(query.get(0))
# 	print(query.count())
# 	for i in query:
# 		print(type(i))
# 		print(i)
# 		# contact = i
# 		# contact.name = 'no name'
# 		# contact.put()