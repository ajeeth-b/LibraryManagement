import pytest
from config import TestConfig
from app.library_manager import *
from random import randint



def get_random_name(size=7):
	chars = map(chr, [randint(97, 122) for i in range(size)])
	return ''.join(chars)


@pytest.mark.skip
@pytest.mark.library_manager
@pytest.mark.book_methods
class TestBookMethods():

	def test_create_invalid_book(self):
		''' creating invalid book '''
		with pytest.raises(BadValueError):
			create_book(1, 1, 1000)

	def test_create_book_and_check(self):
		''' creating valid book, getting it, updating it, deleting it '''
		try:
			book = create_book(get_random_name(), get_random_name(), randint(10, 10000))
			assert type(book) == dict
			assert type(get_book(book['id'])) == dict

			new_name = get_random_name()
			assert type(update_book(book['id'], new_name)) == dict
			assert get_book(book['id'])['name'] == new_name


			assert delete_book(book['id']) is None
			''' deleting again '''
			with pytest.raises(BookNotFound):
				delete_book(book['id'])

		except DuplicateBook:
			assert True

	def test_get_invalid_book(self):
		''' getting book not in db'''
		with pytest.raises(BookNotFound):
			get_book('a')

	def test_get_all_book(self):
		books, cursor, more = get_all_books()
		assert type(books) == list
		assert type(cursor) == str
		assert type(more) == bool

		for i in books:
			assert type(i) == dict

	def test_get_all_book_pagination(self):
		books, cursor, more = get_all_books(per_page=1)
		if more is True:
			books, cursor, more = get_all_books(per_page=1, cursor=cursor)
			''' assert True for successfull retriving of data '''
			assert True
			# assert len(books) > 1

	def test_get_all_book_invalid_cursor(self):
		with pytest.raises(InvalidCursor):
			books, cursor, more = get_all_books(cursor='abcde')


@pytest.mark.skip
@pytest.mark.library_manager
@pytest.mark.member_methods
class TestMemberMethods():

	def test_create_invalid_member(self):
		
		''' creating with bad value '''
		with pytest.raises(BadValueError):
			create_member(1)

	def test_create_member_and_check(self):
		''' creating a valid member '''
		member_name = get_random_name()
		member  = create_member(member_name)
		''' asserting on successfull member creating'''
		assert type(member) == dict
		assert 'id' in member

		''' getting created member'''
		assert get_member(member['id'])['name'] == member_name


		''' deleting create member'''
		assert delete_member(member['id']) is None

		''' deleting again'''
		with pytest.raises(MemberNotFound):
			delete_member(member['id'])

	def test_geting_invalid_member(self):
		''' getting member not in db '''
		with pytest.raises(MemberNotFound):
			get_member('invalid_id')

	def test_get_all_member(self):
		members, cursor, more = get_all_books()
		assert type(members) == list
		assert type(cursor) == str
		assert type(more) == bool

		for i in members:
			assert type(i) == dict

	def test_get_all_member_pagination(self):
		members, cursor, more = get_all_members(per_page=1)
		if more is True:
			member, cursor, more = get_all_members(per_page=1, cursor=cursor)
			''' assert True for successfull retriving of data '''
			assert True
			# assert len(members) > 1

	def test_get_all_member_invalid_cursor(self):
		with pytest.raises(InvalidCursor):
			members, cursor, more = get_all_members(cursor='abcde')

@pytest.mark.skip
@pytest.mark.library_manager
@pytest.mark.library_methods
class TestLibraryMethods():

	def test_get_borrow_data(self):
		data, cursor, more = get_borrow_data(per_page=1)
		''' asserting on successfull query'''
		assert True
		for d in data:
			assert 'book_id' in d
			assert 'member_id' in d


	def test_get_borrow_data_pagination(self):
		data, cursor, more = get_borrow_data(per_page=1)
		if more is True:
			data, cursor, more = get_borrow_data(per_page=1, cursor=cursor)
			''' asserting on successfull query'''
			assert True

	def test_get_borrow_data_invalid_cursor(self):
		with pytest.raises(InvalidCursor):
			data, cursor, more = get_borrow_data(per_page=1, cursor='abcde')

	def test_borrow_book_with_invalid_member(self):
		member  = create_member(get_random_name())
		with pytest.raises(MemberNotFound):
			borrow_book('invalid_book_id', member['id'])
		delete_member(member['id'])

	def test_borrow_book_with_invalid_member(self):
		book = create_book(get_random_name(), get_random_name(), randint(10, 10000))
		with pytest.raises(MemberNotFound):
			borrow_book(book['id'], 'invalid_member_id')
		delete_book(book['id'])

	def test_borrow_and_return_book(self):
		book = create_book(get_random_name(), get_random_name(), randint(10, 10000))
		member  = create_member(get_random_name())

		assert borrow_book(book['id'], member['id']) is None

		''' verifying the borrow'''
		book = get_book(book['id'])
		assert book['taken'] == True
		assert book['taken_by'] == member['id']

		assert return_book(book['id'], member['id']) is None

		''' verifying the returining'''
		book = get_book(book['id'])
		assert book['taken'] == False
		assert book['taken_by'] == None

		''' deleting the data'''
		delete_book(book['id'])
		delete_member(member['id'])