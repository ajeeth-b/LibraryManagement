from flask import Blueprint, jsonify, request
from .library_manager import *
from google.cloud.ndb.exceptions import BadValueError

library = Blueprint('library', __name__, url_prefix='/api')


# Book Actions

@library.route('/library/books', methods=['GET'])
def get_all_books_handler():
    available = request.args.get('available', None)
    cursor = request.args.get('cursor', None)
    per_page = request.args.get('per-page', '10')

    if per_page.isdigit():
        per_page = int(per_page)
    else:
        per_page = 10

    if available == 'true':
        available = True
    elif available == 'false':
        available = False
    else:
        available = None

    try:
        books, next_cursor, more = get_all_books(
            available=available, 
            cursor=cursor,
            per_page=per_page
            )
    except InvalidCursor:
        return jsonify({'status':'failed', 'message':'Invalid Cursor'})
    data = {'status': 'success', 'books':books, 'next_cursor':next_cursor, 'prev_cursor':cursor, 'more':more}
    return jsonify(data)


@library.route('/library/books', methods=['POST'])
def create_new_book_handler():
    data = request.json
    if not (data and all([i in data for i in ['name', 'author', 'isbn']])):
        return jsonify({'status': 'failed', 'message': 'Insufficient data'})
    if type(data['isbn']) != int:
        return jsonify({'status': 'failed', 'message': 'Invalid ISBN'})

    try:
        book = create_book(data['name'], data['author'], data['isbn'])
    except DuplicateBook:
        return jsonify({'status': 'failed', 'message': 'Book with same ISBN already available'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})
    return jsonify({'status': 'success', 'message': 'book added successfully', 'book': book})


@library.route('/library/books/<int:book_id>', methods=['GET'])
def get_book_handler(book_id):
    try:
        book = get_book(book_id)
    except BookNotFound:
        return jsonify({'status': 'failed', 'message': 'Book Not Found'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'book': book})


@library.route('/library/books/<int:book_id>', methods=['PUT'])
def update_book_handler(book_id):
    data = request.json
    if not data:
        return jsonify({'status': 'failed', 'message': 'no data to change'})

    try:
        book = update_book(
            book_id,
            name=data.get('name', None),
            author=data.get('author', None)
        )
    except BookNotFound:
        return jsonify({'status': 'failed', 'message': 'Book Not Found'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'book': book})


@library.route('/library/books/<int:book_id>', methods=['DELETE'])
def delete_book_handler(book_id):
    try:
        delete_book(book_id)
    except BookNotFound:
        return jsonify({'status': 'failed', 'message': 'Book Not Found'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': "success", "message": "book deleted successfully."})


# Member Actions


@library.route('/library/members', methods=['GET'])
def get_all_members_handler():
    cursor = request.args.get('cursor', None)
    per_page = request.args.get('per-page', '10')

    if per_page.isdigit():
        per_page = int(per_page)
    else:
        per_page = 10

    try:
        members, next_cursor, more = get_all_members(
            cursor=cursor,
            per_page=per_page
            )
    except InvalidCursor:
        return jsonify({'status':'failed', 'message':'Invalid Cursor'})
    data = {'status': 'success', 'members':members, 'next_cursor':next_cursor, 'prev_cursor':cursor, "more":more}


    return jsonify(data)


@library.route('/library/members', methods=['POST'])
def create_new_member_handler():
    data = request.json
    if not (data and 'name' in data):
        return jsonify({'status': 'failed', 'message': 'Insufficient data'})

    try:
        member = create_member(data['name'])
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})
    return jsonify({'status': 'success', 'message': 'member added successfully', 'member': member})


@library.route('/library/members/<int:member_id>', methods=['GET'])
@library.route('/library/members/<string:member_id>', methods=['GET'])
def get_member_handler(member_id):
    try:
        member = get_member(member_id)
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})

    return jsonify({'status': 'success', 'member': member})


@library.route('/library/members/<int:member_id>', methods=['PUT'])
@library.route('/library/members/<string:member_id>', methods=['PUT'])
def update_member_handler(member_id):
    data = request.json
    if 'name' not in data:
        return jsonify({'status': 'failed', 'message': 'no data to change'})

    try:
        member = update_member(member_id,
            name=data.get('name'),
        )
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'member': member})


@library.route('/library/members/<int:member_id>', methods=["DELETE"])
@library.route('/library/members/<string:member_id>', methods=["DELETE"])
def delete_member_handler(member_id):
    try:
        delete_member(member_id)
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'message': 'Member deleted successfully.'})

@library.route('/library/members/<int:member_id>/books', methods=['GET'])
@library.route('/library/members/<string:member_id>/books', methods=['GET'])
def books_borrowed_by_member(member_id):

    cursor = request.args.get('cursor', None)
    per_page = request.args.get('per-page', '10')

    if per_page.isdigit():
        per_page = int(per_page)
    else:
        per_page = 10

    try:
        books, next_cursor, more = get_book_borrowed_by_member(
            member_id,
            per_page=per_page,
            cursor=cursor,
            )
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})
    except InvalidCursor:
        return jsonify({'status':'failed', 'message':'Invalid Cursor'})

    return jsonify({'status': 'success', 'books': books, 'next_cursor':next_cursor, 'prev_cursor':cursor, 'more':more})


# Library Actions

@library.route('/library', methods=['GET'])
def get_borrowed_data_handler():
    cursor = request.args.get('cursor', None)
    per_page = request.args.get('per-page', '10')

    if per_page.isdigit():
        per_page = int(per_page)
    else:
        per_page = 10

    try:
        data, next_cursor, more = get_borrow_data(
            per_page=per_page, 
            cursor=cursor,
            )
    except InvalidCursor:
        return jsonify({'status':'failed', 'message':'Invalid Cursor'})

    resp_data = {'status': 'success', 'data': data, 'prev_cursor':cursor, 'next_cursor':next_cursor, 'more':more}
    return jsonify(resp_data)


@library.route('/library', methods=['POST'])
def borrow_book_handler():
    data = request.json
    if not (data and all([i in data for i in ['book_id', 'member_id']])):
        return jsonify({'status': 'failed', 'message': 'Insufficient data'})

    try:
        borrow_book(data['book_id'], data['member_id'])
    except BookNotFound:
        return jsonify({'status': 'failed', 'message': 'Book Not Found'})
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})
    except BookAlreadyTaken:
        return jsonify({'status': 'failed', 'message': 'Book Already Taken'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'message': 'Book borrowed.'})


@library.route('/library', methods=['PUT'])
def return_borrowed_book_handler():
    data = request.json
    if not (data and all([i in data for i in ['book_id', 'member_id']])):
        return jsonify({'status': 'failed', 'message': 'Insufficient data'})

    try:
        return_book(data['book_id'], data['member_id'])
    except BookNotBorrowed:
        return jsonify({'status': 'failed', 'message': 'book not borrowed'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'message': 'book returned'})
