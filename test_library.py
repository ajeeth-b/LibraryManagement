import pytest
from library.library import LibraryManager

library = LibraryManager()


def test_library_creation():
    assert type(library) == LibraryManager


def test_add_member():
    assert library.add_member('ajeeth')


def test_add_empty_member():
    with pytest.raises(ValueError):
        library.add_member('')


def test_add_book():
    assert library.add_book('book1', 1, 'author')


def test_add_empty_book():
    with pytest.raises(ValueError):
        library.add_book('', 0, '')
    with pytest.raises(ValueError):
        library.add_book('book2', 0, '')
    with pytest.raises(ValueError):
        library.add_book('book2', 12, '')


def test_borrow_book():
    assert library.add_member('ajeeth')
    assert library.borrow_book(1, 1) == True
