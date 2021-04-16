import pytest
from library.library_objects import Book, Member


@pytest.mark.book
def test_book_creation():
    assert Book('name', '1', 'author')


@pytest.mark.book
def test_book_creation_with_empty_data():
    # Empty name
    with pytest.raises(ValueError):
        b = Book('', 1, 'author')
    # Empty ISBN
    with pytest.raises(ValueError):
        b = Book('aj', '', 'auth')
    # Empty author name
    with pytest.raises(ValueError):
        b = Book('aj', '10', '')


@pytest.mark.book
def test_book_data_type_change():
    book = Book('bk', 123, 'author')

    # change book name
    with pytest.raises(TypeError):
        book.name = 1

    # change isbn
    with pytest.raises(TypeError):
        book.isbn = []

    # change author
    with pytest.raises(TypeError):
        book.author = 1


@pytest.mark.member
def test_member_creation():
    assert Member('name')


@pytest.mark.member
def test_member_creation_with_empty_data():
    # Empty name
    with pytest.raises(ValueError):
        m = Member('')


@pytest.mark.member
def test_member_data_type_change():
    member = Member('Ajeeth')

    # change member name
    with pytest.raises(TypeError):
        member.name = 1
