from .models import Book, Member, User
from .utils import with_client_context
from google.cloud.ndb import Key, Cursor
from google.cloud.ndb.exceptions import BadValueError
import binascii
from google.api_core.exceptions import InvalidArgument



class BookNotFound(Exception):
    pass


class DuplicateBook(Exception):
    pass


class BookAlreadyTaken(Exception):
    pass


class MemberNotFound(Exception):
    pass


class BookNotBorrowed(Exception):
    pass

class InvalidCursor(Exception):
    pass


# Book Operations

@with_client_context
def create_book(name, author, isbn):
    book = Book.query().filter(Book.isbn == isbn)
    if book.count() != 0:
        raise DuplicateBook()
    if type(isbn) != int:
        raise BadValueError()
    book = Book(name=name, author=author, isbn=isbn)
    book.put()
    return book.get_dict()

@with_client_context
def get_book(book_id):
    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()
    return book.get_dict()  

@with_client_context
def get_all_books(available = None, per_page=10, cursor=None):

    query = Book.query()
    if available is not None:
        available = not(available)
        query = query.filter(Book.taken == available)

    try:
        cursor = Cursor(urlsafe=cursor)
        books, new_cursor, more = query.fetch_page(per_page, start_cursor=cursor)
    except (binascii.Error, InvalidArgument):
        raise InvalidCursor()
    
    if new_cursor is not None:
        new_cursor = new_cursor.urlsafe().decode('utf-8')

    books = [book.get_dict() for book in books]
    return books, new_cursor, more


@with_client_context
def update_book(book_id, name=None, author=None):
    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()
    if name is not None:
        book.name = name
    if author is not None:
        book.author = author
    book.put()
    return book.get_dict()


@with_client_context
def delete_book(book_id):
    
    key = Key(Book, book_id)
    if key.get() is None:
        raise BookNotFound()
    key.delete()


# Member Operations

@with_client_context
def create_member(name):
    member = Member(name=name)
    member.put()

    return member.get_dict()


@with_client_context
def get_member(member_id):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()

    return member.get_dict()


@with_client_context
def get_all_members(per_page=10, cursor=None):

    try:
        cursor = Cursor(urlsafe=cursor)
        members, new_cursor, more = Member.query().fetch_page(per_page, start_cursor=cursor)
    except (binascii.Error, InvalidArgument):
        raise InvalidCursor()

    if new_cursor:
        new_cursor = new_cursor.urlsafe().decode('utf-8')
    members = [member.get_dict() for member in members]
    return members, new_cursor, more

@with_client_context
def update_member(member_id, name=None):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()
    if name is not None:
        member.name = name
    member.put()
    return member.get_dict()


@with_client_context
def delete_member(member_id):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()
    member.key.delete()


@with_client_context
def get_book_borrowed_by_member(member_id, per_page=10, cursor=None):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()

    query = Book.query().filter(Book.taken_by == member.key)

    try:
        cursor = Cursor(urlsafe=cursor)
        books, new_cursor, more = query.fetch_page(
            per_page, 
            start_cursor=cursor,
            projection = [Book.name, Book.isbn, Book.author]
            )
    except (binascii.Error, InvalidArgument):
        raise InvalidCursor()

    if new_cursor is not None:
        new_cursor = new_cursor.urlsafe().decode('utf-8')

    books = [book.get_dict() for book in books]
    return books, new_cursor, more


# Library Operations

@with_client_context
def get_borrow_data(per_page=10, cursor=None):
    query = Book.query().filter(Book.taken == True)

    try:
        cursor = Cursor(urlsafe=cursor)
        data, new_cursor, more = query.fetch_page(per_page, start_cursor=cursor, projection=[Book.taken_by])
    except (binascii.Error, InvalidArgument):
        raise InvalidCursor()

    if new_cursor is not None:
        new_cursor = new_cursor.urlsafe().decode('utf-8')

    return [{'book_id':i.key.id(), 'member_id':i.taken_by.id()} for i in data], new_cursor, more



@with_client_context
def borrow_book(book_id, member_id):

    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()

    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()
    if book.taken == True:
        raise BookAlreadyTaken()

    book.taken_by = member.key
    book.taken = True
    book.put()



@with_client_context
def return_book(book_id, member_id):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()

    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()

    if book.taken_by != member.key:
        raise BookNotBorrowed()

    book.taken_by = None
    book.taken = False
    book.put()
