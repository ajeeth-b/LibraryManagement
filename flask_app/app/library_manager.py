from .models import Book, Member, Borrow
from .utils import with_client_context
from google.cloud.ndb import Key, Cursor


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


# Book Operations

@with_client_context
def create_book(name, author, isbn):
    book = Book.query().filter(Book.isbn == isbn)
    if book.count() != 0:
        raise DuplicateBook()
    book = Book(name=name, author=author, isbn=isbn)
    book.put()
    return {**book.to_dict(), **{'id':book.key.id()}}

@with_client_context
def query_book(book_id):
    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()
    return {**book.to_dict(), **{'id':book.key.id()}}  

@with_client_context
def get_all_books(available=False, per_page=10, cursor=None):
    data = []

    query = Book.query()

    if available:
        for i in Borrow.query().filter(Borrow.returned == False).fetch(projection=['book_id']):
            query = query.filter(Book.isbn != i.book_id)

    books, new_cursor, has_next = query.fetch_page(per_page, start_cursor=Cursor(urlsafe=cursor))

    print(new_cursor, has_next)

    if new_cursor is not None:
        new_cursor = new_cursor.urlsafe().decode('utf-8')

    books = [{**book.to_dict(), **{'id':book.key.id()}} for book in books]
    return books, new_cursor, has_next


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
    return {**book.to_dict(), **{'id':book.key.id()}}


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

    return {**member.to_dict(),**{'id':member.key.id()}}


@with_client_context
def query_member(member_id):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()

    return {**member.to_dict(),**{'id':member.key.id()}}


@with_client_context
def get_all_members(per_page=10, cursor=None):
    members, new_cursor, has_more = Member.query().fetch_page(per_page, start_cursor=Cursor(urlsafe=cursor))
    
    if new_cursor:
        new_cursor = new_cursor.urlsafe().decode('utf-8')
    members = [{**member.to_dict(), **{'id':member.key.id()}} for member in members]
    return members, new_cursor, has_more

@with_client_context
def update_member(member_id, name=None):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound
    if name is not None:
        member.name = name
    member.put()
    return {**member.to_dict(),**{'id':member.key.id()}}


@with_client_context
def delete_member(member_id):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound
    member.key.delete()


@with_client_context
def get_book_borrowed_by_member(member_id):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound
    borrowed_books_id = Borrow.query().filter(Borrow.member_id == member_id, Borrow.returned == False)
    borrowed_books_id = [i.book_id for i in borrowed_books_id]
    return borrowed_books_id


# Library Operations

@with_client_context
def borrow_data(borrow_filter=None, per_page=10, cursor=None):
    query = Borrow.query()
    if borrow_filter is not None:
        query = query.filter(Borrow.returned == borrow_filter)

    if cursor is not None:
        cursor = Cursor(urlsafe=cursor)

    data, new_cursor, has_more = query.fetch_page(per_page, start_cursor=cursor)

    if new_cursor is not None:
        new_cursor = new_cursor.urlsafe().decode('utf-8')
    return [{**i.to_dict(), **{'id':i.key.id()}} for i in data], new_cursor, has_more


@with_client_context
def borrow_book(book_id, member_id):
    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()

    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()

    already_borrowed = Borrow.query().filter(
        Borrow.book_id == book_id,
        Borrow.member_id == member_id,
        Borrow.returned == False
    )
    if already_borrowed.count() != 0:
        raise BookAlreadyTaken()

    borrow = Borrow(book_id=book_id, member_id=member_id, returned=False)
    borrow.put()


@with_client_context
def return_book(book_id, member_id):
    borrowed_data = Borrow.query().filter(
        Borrow.book_id == book_id,
        Borrow.member_id == member_id,
        Borrow.returned == False
    )
    if borrowed_data.count() == 0:
        raise BookNotBorrowed()

    borrowed_data = borrowed_data.get(0)
    borrowed_data.returned = True
    borrowed_data.put()

