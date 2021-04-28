from .models import Book, Member
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
    return book.get_dict()

@with_client_context
def query_book(book_id):
    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()
    return book.get_dict()  

@with_client_context
def get_all_books(available=False, per_page=10, cursor=None):
    data = []

    query = Book.query()

    # if available:
    #     for i in Borrow.query().filter(Borrow.returned == False).fetch(projection=['book_id']):
    #         query = query.filter(Book.isbn != i.book_id)

    books, new_cursor, has_next = query.fetch_page(per_page, start_cursor=Cursor(urlsafe=cursor))

    temp_book, temp_cursor, has_next = query.fetch_page(1, start_cursor=new_cursor)
    
    if not has_next:
        new_cursor = None

    if new_cursor is not None:
        new_cursor = new_cursor.urlsafe().decode('utf-8')

    books = [book.get_dict() for book in books]
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
        raise MemberNotFound()
    
    books = Books.query().filter(Book.key == member.key)
    books = [{**book.to_dict(), **{'id':book.key.id()}} for book in books]
    return books


# Library Operations

@with_client_context
def borrow_data(per_page=10, cursor=None):
    query = Book.query().filter(Book.taken_by != None)

    if cursor is not None:
        cursor = Cursor(urlsafe=cursor)

    data, new_cursor, has_more = query.fetch_page(per_page, start_cursor=cursor, projection=[Book.isbn])

    if new_cursor is not None:
        new_cursor = new_cursor.urlsafe().decode('utf-8')

    return [i.get_dict() for i in data], new_cursor, has_more


@with_client_context
def borrow_data(per_page=10, offset=0):
    query = Book.query().filter(Book.taken_by != None)
    books = query.fetch(per_page, offset=offset)

    offset += len(books)
    has_more = True
    if query.count() <= offset:
        offset = None
        has_more = False
    
    return [i.get_dict() for i in books], offset, has_more


@with_client_context
def borrow_book(book_id, member_id):

    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()

    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()
    if book.taken_by is not None:
        raise BookAlreadyTaken()

    book.taken_by = member.key
    book.put()



@with_client_context
def return_book(book_id, member_id):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()

    book = Book.get_by_id(book_id)
    if book is None:
        raise BookNotFound()

    if book.taken_by is  None:
        raise BookNotBorrowed()

    book.taken_by = None
    book.put()


# @with_client_context
# def temp():
#     query = Book.query()
#     from sys import getsizeof
#     print(dir(query))
#     print(getsizeof(query))
#     total = 0
#     for i in query:
#         total += getsizeof(i)
#     print(total)

# temp()