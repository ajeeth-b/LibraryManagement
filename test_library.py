import pytest
from library.library import LibraryManager


class TestLibrary:

    def setup(self):
        self.library = LibraryManager()

    def test_library_creation(self):
        assert type(self.library) == LibraryManager

    def test_add_member(self):
        assert self.library.add_member('ajeeth')

    def test_add_empty_member(self):
        with pytest.raises(ValueError):
            self.library.add_member('')

    def test_add_book(self):
        assert self.library.add_book('book1', 1, 'author')

    def test_add_empty_book(self):
        with pytest.raises(ValueError):
            self.library.add_book('', 0, '')
        with pytest.raises(ValueError):
            self.library.add_book('book2', 0, '')
        with pytest.raises(ValueError):
            self.library.add_book('book2', 12, '')

    def test_borrow_book(self):
        assert self.library.borrow_book(1, 1) == True
