from .models import Book, Member, Borrow
from .utils import with_client_context
from uuid import uuid4


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
    return book.to_dict()

@with_client_context
def query_book(book_id):
    book = Book.query().filter(Book.isbn == book_id)
    if book.count() == 0:
        raise BookNotFound()
    return book.get(0).to_dict()

@with_client_context
def get_all_books(available=False):
    data = []

    query = Book.query()

    if available:
        for i in Borrow.query().filter(Borrow.returned == False).fetch(projection=['book_id']):
            query = query.filter(Book.isbn != i.book_id)

    for i in query:
        data.append(i.to_dict())
    return data


@with_client_context
def update_book(book_id, name=None, author=None):
    book = Book.query().filter(Book.isbn == book_id)
    if book.count() == 0:
        raise BookNotFound
    book = book.get(0)
    if name is not None:
        book.name = name
    if author is not None:
        book.author = author
    book.put()
    return book.to_dict()


@with_client_context
def delete_book(book_id):
    book = Book.query().filter(Book.isbn == book_id)
    if book.count() == 0:
        raise BookNotFound
    book.get(0).key.delete()


# Member Operations

@with_client_context
def create_member(name):
    member_id = str(uuid4())
    member = Member(id= member_id, name=name)
    member.put()

    member_data = member.to_dict()
    member_data.update({'id':member_id})
    
    return member_data


@with_client_context
def query_member(member_id):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound()
    data = member.to_dict()
    data['id'] = member.key.id()
    return data


@with_client_context
def get_all_members():
    data = []
    for i in Member.query():
        member = i.to_dict()
        member['id'] = i.key.id()
        data.append(member)
    return data

@with_client_context
def update_member(member_id, name=None):
    member = Member.get_by_id(member_id)
    if member is None:
        raise MemberNotFound
    if name is not None:
        member.name = name
    member.put()
    return member.to_dict()


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
def borrow_data(borrow_filter=None):
    data = Borrow.query()
    if borrow_filter is not None:
        data = data.filter(Borrow.returned == borrow_filter)
    return [i.to_dict() for i in data]


@with_client_context
def borrow_book(book_id, member_id):
    book = Book.query().filter(Book.isbn == book_id)
    if book.count() == 0:
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

