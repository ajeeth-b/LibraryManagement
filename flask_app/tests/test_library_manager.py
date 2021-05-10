import pytest
import mock
from app.library_manager import *
from app.models import Book, Member
from google.cloud.ndb.query import Query


def test_create_book(mocker):
    # testing for creating valid book
    mocker_query_count = mocker.patch('google.cloud.ndb.query.Query.count', return_value=0)
    mocker_model_put = mocker.patch('google.cloud.ndb.Model.put')
    mocker_book_get_dict = mocker.patch('app.models.Book.get_dict',
                                        return_value={'name': 'name', "author": 'author', "isbn": 1})
    try:
        create_book('name', 'author', 1)
        assert True
    except:
        pytest.fail('Error in creating a valid book')

    # Testing by creating duplicate book
    mocker_query_count = mocker.patch('google.cloud.ndb.query.Query.count', return_value=1)
    with pytest.raises(DuplicateBook):
        create_book('name', 'author', 1)

    # Testing by giving bad value
    mocker_query_count = mocker.patch('google.cloud.ndb.query.Query.count', return_value=0)
    with pytest.raises(BadValueError):
        create_book('name', 'author', 'a')
    with pytest.raises(BadValueError):
        create_book(1, 'author', 1)
    with pytest.raises(BadValueError):
        create_book('name', 100, 1)


def test_get_book(mocker):
    mocker_book_get_dict = mocker.patch('app.models.Book.get_dict',
                                        return_value={'name': 'name', "author": 'author', "isbn": 1})

    # Testing for getting a valid book
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=Book())
    try:
        get_book(1)
    except Exception as e:
        pytest.fail('Error in getting a valid book' + str(e))
    mocker_model_get_by_id.assert_called_once()

    # Testing geting book that is not found
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=None)
    with pytest.raises(BookNotFound):
        get_book(1)


def test_get_all_books(mocker):
    # Testing the proper execution without any error
    mocker_book_get_dict = mocker.patch('app.models.Book.get_dict',
                                        return_value={'name': 'name', "author": 'author', "isbn": 1})
    mocker_query_fetch_page = mocker.patch('google.cloud.ndb.query.Query.fetch_page', return_value=([], None, False))
    try:
        get_all_books()
        assert True
    except Exception as e:
        pytest.fail('Error on making a proper call of the function' + str(e))
    mocker_query_fetch_page.assert_called_once()

    # Testing with Invalid cursor
    with pytest.raises(InvalidCursor):
        get_all_books(cursor='invalidcursor')

    # Testing to get available book -> "avaiable = True" parameter
    mocker_query_filter = mocker.patch('google.cloud.ndb.query.Query.filter', return_value=Query())
    get_all_books(available=True)
    assert mocker_query_filter.call_count != 0


def test_update_book(mocker):
    mocker_model_put = mocker.patch('google.cloud.ndb.Model.put')

    # Testing for Invalid Book
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=None)
    with pytest.raises(BookNotFound):
        update_book(1)

    # Testing for bad values
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=Book())
    with pytest.raises(BadValueError):
        update_book(1, name=1)

    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=Book())
    with pytest.raises(BadValueError):
        update_book(1, author=123)

    # Testing for proper updation
    mocker_book_get_dict = mocker.patch('app.models.Book.get_dict',
                                        return_value={'name': 'name', "author": 'author', "isbn": 1})
    try:
        update_book(1, name='name', author='author')
    except Exception as e:
        pytest.fail('Error in proper updation of book ' + str(e))


def test_delete_book(mocker):
    mocker_ndb_key_get = mocker.patch('google.cloud.ndb.Key.get', return_value=None)
    with pytest.raises(BookNotFound):
        delete_book(1)


'''Testing Member methods'''


def test_create_member(mocker):
    # Testing creation of member
    mocker_model_put = mocker.patch('google.cloud.ndb.Model.put')
    mocker_member_get_dict = mocker.patch('app.models.Member.get_dict', return_value={'name': 'name', 'id': 1})
    try:
        create_member(name='Ajeeth')
        mocker_model_put.assert_called_once()
        mocker_member_get_dict.assert_called_once()
    except Exception as e:
        pytest.fail('Error in proper creation of member ' + str(e))

    # Testig with bad value
    with pytest.raises(BadValueError):
        create_member(name=1)


def test_get_member(mocker):
    mocker_member_get_dict = mocker.patch('app.models.Member.get_dict', return_value={'name': 'name'})

    # Testing for getting a valid member
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=Member())
    try:
        get_member(1)
    except Exception as e:
        pytest.fail('Error in getting a valid member' + str(e))
    mocker_model_get_by_id.assert_called_once()

    # Testing geting member that is not found
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=None)
    with pytest.raises(MemberNotFound):
        get_member(1)


def test_get_all_members(mocker):
    # Testing the proper execution without any error
    mocker_member_get_dict = mocker.patch('app.models.Member.get_dict',
                                          return_value={'name': 'name', "author": 'author', "isbn": 1})
    mocker_query_fetch_page = mocker.patch('google.cloud.ndb.query.Query.fetch_page', return_value=([], None, False))
    try:
        get_all_members()
        assert True
    except Exception as e:
        pytest.fail('Error on making a proper call of the function' + str(e))
    mocker_query_fetch_page.assert_called_once()

    # Testing with Invalid cursor
    with pytest.raises(InvalidCursor):
        get_all_members(cursor='invalidcursor')


def test_update_member(mocker):
    mocker_model_put = mocker.patch('google.cloud.ndb.Model.put')

    # Testing for Invalid Member
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=None)
    with pytest.raises(MemberNotFound):
        update_member(1)

    # Testing for bad values
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=Member())
    with pytest.raises(BadValueError):
        update_member(1, name=1)

    # Testing for proper updation
    mocker_member_get_dict = mocker.patch('app.models.Member.get_dict',
                                          return_value={'name': 'name', "author": 'author', "isbn": 1})
    try:
        update_member(1, name='name')
    except Exception as e:
        pytest.fail('Error in proper updation of member ' + str(e))


def test_delete_member(mocker):
    mocker_ndb_key_get = mocker.patch('google.cloud.ndb.Key.get', return_value=None)
    with pytest.raises(MemberNotFound):
        delete_member(1)


def test_get_book_borrowed_by_member(mocker):
    # Testing for invalid member
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=None)
    with pytest.raises(MemberNotFound):
        get_book_borrowed_by_member(1)

    # Testing Invalid cursor
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=Member())
    mocker_query_filter = mocker.patch('google.cloud.ndb.query.Query.filter', return_value=Query())
    with pytest.raises(InvalidCursor):
        get_book_borrowed_by_member(1, cursor='invalidcursor')

    # Testing with proper data
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=Member())
    mocker_query_filter = mocker.patch('google.cloud.ndb.query.Query.filter', return_value=Query())
    mocker_query_fetch_page = mocker.patch('google.cloud.ndb.query.Query.fetch_page', return_value=([], None, False))
    try:
        get_book_borrowed_by_member(1)
    except Exception as e:
        pytest.fail('Error in proper calling of function' + str(e))


def test_get_borrow_data(mocker):
    mocker_query_filter = mocker.patch('google.cloud.ndb.query.Query.filter', return_value=Query())
    mocker_query_fetch_page = mocker.patch('google.cloud.ndb.query.Query.fetch_page', return_value=([], None, False))

    # Test proper call of function
    try:
        get_borrow_data()
        assert True
    except Exception as e:
        pytest.fail('Error in get_borrow_data ' + str(e))

    with pytest.raises(InvalidCursor):
        get_borrow_data(cursor='invalidcursor')


def test_borrow_book(mocker):
    # Testing with Invalid member
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id')
    mocker_model_get_by_id.side_effect = [None, None]
    with pytest.raises(MemberNotFound):
        borrow_book(1, 2)

    # Testing with Invalid Book
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id')
    mocker_model_get_by_id.side_effect = [Member(), None]
    with pytest.raises(BookNotFound):
        borrow_book(1, 2)

    # Testing with Already Taken Book
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id')
    mocker_model_get_by_id.side_effect = [Member(), Book(taken=True)]
    with pytest.raises(BookAlreadyTaken):
        borrow_book(1, 2)

    # Testing proper calling of function
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id')
    book = Book(taken=False)
    mocker_model_get_by_id.side_effect = [Member(), book]
    mocker_model_put = mocker.patch('google.cloud.ndb.Model.put')
    borrow_book(1, 2)
    assert book.taken == True
    mocker_model_put.assert_called_once()


def test_return_book(mocker):
    # Testing with Invalid member
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id')
    mocker_model_get_by_id.side_effect = [None, None]
    with pytest.raises(MemberNotFound):
        return_book(1, 2)

    # Testing with Invalid Book
    mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id')
    mocker_model_get_by_id.side_effect = [Member(), None]
    with pytest.raises(BookNotFound):
        return_book(1, 2)

# # Testing with return book by member not taken it
# mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id')
# member = Member()
# member.key = Key(Member, 1)
# book = Book(taken=True, taken_by=Key(Member, 2))
# mocker_model_get_by_id.side_effect = [member, book]
# with pytest.raises(BookNotBorrowed):
# 	return_book(1,2)

# # Testing proper calling of function
# mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id')
# book = Book(taken=False)
# mocker_model_get_by_id.side_effect = [Member(), book]
# mocker_model_put = mocker.patch('google.cloud.ndb.Model.put')
# return_book(1,2)
# assert book.taken == True
# mocker_model_put.assert_called_once()
