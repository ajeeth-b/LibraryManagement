
class Member(object):

	def __init__(self, name):
		self.name = name

class Book(object):

	def __init__(self, name, isbn, author):
		self.name   = name
		self.isbn   = isbn
		self.author = author



class MemberManager(object):
	__next_id = 1

	def __init__(self):
		self.members = {}

	def add_member(self, member):
		self.members[MemberManager.__next_id] = member
		print(f'Member added successfully.\nMember ID is {MemberManager.__next_id}')
		MemberManager.__next_id += 1

	def get_all_member(self):
		return self.members.keys()

	def get_member(self, member_id):
		if member_id not in self.members:
			return None
		return self.members[member_id]

	def delete_member(self, member_id):
		if member_id not in self.members:
			print('Member not found')
		else:
			del self.members[member_id]
			print('Member deleted successfully')


class BookManager(object):

	__next_id = 1

	def __init__(self):
		self.books = {}

	def add_book(self, book):
		self.books[BookManager.__next_id] = book
		print(f'Book added successfully.\nBook ID is {BookManager.__next_id}')
		BookManager.__next_id += 1

	def get_all_books(self):
		return self.books.keys()

	def get_book(self, book_id):
		if book_id not in self.books:
			return None
		return self.books[book_id]

	def delete_book(self, book_id):
		if book_id not in self.books:
			print('Book not found')
		else:
			del self.books[book_id]
			print('Book deleted successfully')

	def show_books_excpet(self, book_id_list):
		return list(set(self.books.keys())-set(book_id_list))