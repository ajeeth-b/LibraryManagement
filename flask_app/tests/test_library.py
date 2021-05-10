import pytest
import mock
from app.library_manager import *


@mock.patch('app.library.get_all_books')
def test_get_all_books(mocker_get_all_book, app):
    mocker_get_all_book.return_value = (['data'], 'invalid cursor', True)
    resp = app.get('/api/library/books')

    assert resp.status_code == 200
    mocker_get_all_book.asssert_called_once()
    assert mocker_get_all_book.call_args_list[0].kwargs == {'available': None, 'cursor': None, 'per_page': 10}

    ''' Testing for InvalidCursor '''
    expected = {'status': 'failed', 'message': 'Invalid Cursor'}
    mocker_get_all_book.side_effect = InvalidCursor()
    resp = app.get('/api/library/books')
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.create_book')
def test_create_new_book_handler(mocker_create_book, app):
    ''' Test with insufficient data'''
    data = {'name': 'name', 'author': 'author'}
    expected = {'status': 'failed', 'message': 'Insufficient data'}
    resp = app.post('/api/library/books', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Test with invalid ISBN'''
    data = {'name': 'name', 'author': 'author', 'isbn': 'string'}
    expected = {'status': 'failed', 'message': 'Invalid ISBN'}
    resp = app.post('/api/library/books', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Test with valid data '''
    data = {'name': 'name', 'author': 'author', 'isbn': 1}
    expected = {'status': 'success', 'message': 'book added successfully', 'book': data}
    mocker_create_book.return_value = data
    resp = app.post('/api/library/books', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing with raising DuplicateBook Error '''
    data = {'name': 'name', 'author': 'author', 'isbn': 1}
    expected = {'status': 'failed', 'message': 'Book with same ISBN already available'}
    mocker_create_book.side_effect = DuplicateBook()
    resp = app.post('/api/library/books', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing with raising BadValueError Error '''
    data = {'name': 'name', 'author': 'author', 'isbn': 1}
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_create_book.side_effect = BadValueError()
    resp = app.post('/api/library/books', json=data)
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.get_book')
def test_get_book_handler(mocker_get_book, app):
    ''' Testing to get proper response '''
    book = {'name': 'name'}
    expected = {'status': 'success', 'book': book}
    mocker_get_book.return_value = book
    resp = app.get('/api/library/books/1')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BookNotFound '''
    expected = {'status': 'failed', 'message': 'Book Not Found'}
    mocker_get_book.side_effect = BookNotFound()
    resp = app.get('/api/library/books/1')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BadValueError '''
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_get_book.side_effect = BadValueError()
    resp = app.get('/api/library/books/1')
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.update_book')
def test_update_book_handler(mocker_update_book, app):
    ''' Testing with no data '''
    expected = {'status': 'failed', 'message': 'no data to change'}
    mocker_update_book.side_effect = BookNotFound()
    resp = app.put('/api/library/books/1')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing with proper data '''
    book = {'name': 'name1'}
    expected = {'status': 'success', 'book': book}
    mocker_update_book.side_effect = None
    mocker_update_book.return_value = book
    resp = app.put('/api/library/books/1', json=book)
    assert mocker_update_book.call_args.args == (1,)
    assert mocker_update_book.call_args.kwargs == {'name': 'name1', 'author': None}
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BookNotFound '''
    book = {'name': 'name1'}
    expected = {'status': 'failed', 'message': 'Book Not Found'}
    mocker_update_book.side_effect = None
    mocker_update_book.side_effect = BookNotFound()
    resp = app.put('/api/library/books/1', json=book)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BadValueError '''
    book = {'name': 'name1'}
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_update_book.side_effect = None
    mocker_update_book.side_effect = BadValueError()
    resp = app.put('/api/library/books/1', json=book)
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.delete_book')
def test_delete_book_handler(mocker_delete_book, app):
    ''' Testing with proper data '''
    expected = {'status': "success", "message": "book deleted successfully."}
    resp = app.delete('/api/library/books/1')
    assert mocker_delete_book.call_args.args == (1,)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BookNotFound '''
    expected = {'status': 'failed', 'message': 'Book Not Found'}
    mocker_delete_book.side_effect = BookNotFound()
    resp = app.delete('/api/library/books/1')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BadValueError '''
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_delete_book.side_effect = BadValueError()
    resp = app.delete('/api/library/books/1')
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.get_all_members')
def test_get_all_members(mocker_get_all_member, app):
    mocker_get_all_member.return_value = (['data'], 'invalid cursor', True)

    resp = app.get('/api/library/members')
    assert resp.status_code == 200
    mocker_get_all_member.asssert_called_once()
    assert mocker_get_all_member.call_args_list[0].kwargs == {'cursor': None, 'per_page': 10}

    ''' Testing for InvalidCursor '''
    expected = {'status': 'failed', 'message': 'Invalid Cursor'}
    mocker_get_all_member.side_effect = InvalidCursor()
    resp = app.get('/api/library/members')
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.create_member')
def test_create_new_member_handler(mocker_create_member, app):
    ''' Test with insuficcient data'''
    data = {}
    expected = {'status': 'failed', 'message': 'Insufficient data'}
    resp = app.post('/api/library/members', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Test with valid data '''
    data = {'name': 'name'}
    expected = {'status': 'success', 'message': 'member added successfully', 'member': data}
    mocker_create_member.return_value = data
    resp = app.post('/api/library/members', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing with raising BadValueError Error '''
    data = {'name': 'name'}
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_create_member.side_effect = BadValueError()
    resp = app.post('/api/library/members', json=data)
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.get_member')
def test_get_member_handler(mocker_get_member, app):
    ''' Testing to get proper response '''
    member = {'name': 'name'}
    expected = {'status': 'success', 'member': member}
    mocker_get_member.return_value = member
    resp = app.get('/api/library/members/1')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for MemberNotFound '''
    expected = {'status': 'failed', 'message': 'Member Not Found'}
    mocker_get_member.side_effect = MemberNotFound()
    resp = app.get('/api/library/members/1')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BadValueError '''
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_get_member.side_effect = BadValueError()
    resp = app.get('/api/library/members/1')
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.update_member')
def test_update_member_handler(mocker_update_member, app):
    ''' Testing with no data '''
    expected = {'status': 'failed', 'message': 'no data to change'}
    resp = app.put('/api/library/members/1')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing with proper data '''
    member = {'name': 'name1'}
    expected = {'status': 'success', 'member': member}
    mocker_update_member.side_effect = None
    mocker_update_member.return_value = member
    resp = app.put('/api/library/members/1', json=member)
    assert mocker_update_member.call_args.args == (1,)
    assert mocker_update_member.call_args.kwargs == {'name': 'name1'}
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for MemberNotFound '''
    member = {'name': 'name1'}
    expected = {'status': 'failed', 'message': 'Member Not Found'}
    mocker_update_member.side_effect = None
    mocker_update_member.side_effect = MemberNotFound()
    resp = app.put('/api/library/members/1', json=member)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BadValueError '''
    member = {'name': 'name1'}
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_update_member.side_effect = None
    mocker_update_member.side_effect = BadValueError()
    resp = app.put('/api/library/members/1', json=member)
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.delete_member')
def test_delete_member_handler(mocker_delete_member, app):
    ''' Testing with proper data '''
    expected = {'status': 'success', 'message': 'Member deleted successfully.'}
    resp = app.delete('/api/library/members/1')
    assert mocker_delete_member.call_args.args == (1,)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for MemberNotFound '''
    expected = {'status': 'failed', 'message': 'Member Not Found'}
    mocker_delete_member.side_effect = MemberNotFound()
    resp = app.delete('/api/library/members/1')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for BadValueError '''
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_delete_member.side_effect = BadValueError()
    resp = app.delete('/api/library/members/1')
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.get_book_borrowed_by_member')
def test_books_borrowed_by_member(mocker_get_book_borrowed_by_member, app):
    ''' Testing with proper data '''
    mocker_get_book_borrowed_by_member.return_value = (['data'], 'invalid cursor', True)
    resp = app.get('/api/library/members/1/books')

    assert resp.status_code == 200

    ''' Testing for MemberNotFound '''
    mocker_get_book_borrowed_by_member.side_effect = MemberNotFound()
    expected = {'status': 'failed', 'message': 'Member Not Found'}
    resp = app.get('/api/library/members/1/books')
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for InvalidCursor '''
    expected = {'status': 'failed', 'message': 'Invalid Cursor'}
    mocker_get_book_borrowed_by_member.side_effect = InvalidCursor()
    resp = app.get('/api/library/members/1/books')
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.get_borrow_data')
def test_get_library_data(mock_get_borrow_data, app):
    mock_get_borrow_data.return_value = (['data'], 'invalid cursor', True)

    resp = app.get('/api/library')
    assert resp.status_code == 200

    ''' Testing for InvalidCursor '''
    expected = {'status': 'failed', 'message': 'Invalid Cursor'}
    mock_get_borrow_data.side_effect = InvalidCursor()
    resp = app.get('/api/library')
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.borrow_book')
def test_borrow_book_handler(mocker_borrow_book, app):
    ''' Testing with insuficcient data '''
    data = {'book_id': 1}
    expected = {'status': 'failed', 'message': 'Insufficient data'}
    resp = app.post('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing with proper data '''
    data = {'book_id': 1, 'member_id': 2}
    expected = {'status': 'success', 'message': 'Book borrowed.'}
    resp = app.post('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for  BookNotFound'''
    expected = {'status': 'failed', 'message': 'Book Not Found'}
    mocker_borrow_book.side_effect = BookNotFound()
    resp = app.post('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for  MemberNotFound'''
    expected = {'status': 'failed', 'message': 'Member Not Found'}
    mocker_borrow_book.side_effect = MemberNotFound()
    resp = app.post('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for  BookAlreadyTaken '''
    expected = {'status': 'failed', 'message': 'Book Already Taken'}
    mocker_borrow_book.side_effect = BookAlreadyTaken()
    resp = app.post('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for  BadValueError'''
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_borrow_book.side_effect = BadValueError()
    resp = app.post('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected


@mock.patch('app.library.return_book')
def test_return_borrowed_book_handler(mocker_return_book, app):
    ''' Testing with insuficcient data '''
    data = {'book_id': 1}
    expected = {'status': 'failed', 'message': 'Insufficient data'}
    resp = app.put('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing with proper data '''
    data = {'book_id': 1, 'member_id': 2}
    expected = {'status': 'success', 'message': 'book returned'}
    resp = app.put('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for  BookNotBorrowed'''
    expected = {'status': 'failed', 'message': 'book not borrowed'}
    mocker_return_book.side_effect = BookNotBorrowed()
    resp = app.put('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected

    ''' Testing for  BadValueError'''
    expected = {'status': 'failed', 'message': 'Bad Value'}
    mocker_return_book.side_effect = BadValueError()
    resp = app.put('/api/library', json=data)
    assert resp.is_json
    assert resp.json == expected
