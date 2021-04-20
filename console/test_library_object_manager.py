import pytest
from library.library_objects import BookManager, MemberManager, Book, Member

book_m = BookManager()


@pytest.mark.manager
def create_random_books(count=3):
    books = []
    for i in map(str, range(count)):
        books += [Book('book' + i, i, 'author' + i)]
    return books


@pytest.mark.manager
def test_create_book_manager():
    assert BookManager()


@pytest.mark.manager
def test_add_book_to_book_manager():
    books = create_random_books(3)
    for book_index, book in enumerate(books):
        assert type(book_m.add_book(book)) == int
        assert book_index + 1 == len(book_m.get_all_books())


@pytest.mark.manager
def test_adding_unknown_object_book_manager():
    with pytest.raises(TypeError):
        book_m.add_book(dict())


@pytest.mark.manager
def test_get_book_from_manager():
    book_id = book_m.add_book(create_random_books(1)[0])
    assert type(book_m.get_book(book_id)) == Book


member_m = MemberManager()


@pytest.mark.manager
def create_random_members(count=3):
    return [Member('member' + str(i)) for i in range(count)]


@pytest.mark.manager
def test_member_manager_creation():
    assert type(member_m) == MemberManager


@pytest.mark.manager
def test_adding_member_to_manager():
    for member in create_random_members(3):
        assert type(member_m.add_member(member)) == int


@pytest.mark.manager
def test_adding_invalid_member_to_manager():
    with pytest.raises(TypeError):
        member_m.add_member(list())


@pytest.mark.manager
def test_get_member_from_manager():
    member_id = member_m.add_member(create_random_members(1)[0])
    assert type(member_m.get_member(member_id)) == Member
