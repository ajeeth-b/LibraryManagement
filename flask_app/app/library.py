from flask import Blueprint, jsonify, request
from .library_manager import *
from google.cloud.ndb.exceptions import BadValueError

library = Blueprint('library', __name__, url_prefix='/api')


# Book Actions

@library.route('/library/books', methods=['GET'])
def get_all_books_handler():
    available = request.args.get('available', True)
    if available != 'true':
        available = False
    return jsonify({'books': get_all_books(available)})


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
        book = query_book(book_id)
    except BookNotFound:
        return jsonify({'status': 'failed', 'message': 'Book Not Found'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'book': book})


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

    return jsonify({'book': book})


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
    return jsonify({'members': get_all_members()})


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


@library.route('/library/members/<uuid:member_id>', methods=['GET'])
def get_member_handler(member_id):
    try:
        member = query_member(str(member_id))
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})

    return jsonify({'member': member})


@library.route('/library/members/<uuid:member_id>', methods=['PUT'])
def update_member_handler(member_id):
    data = request.json
    if 'name' not in data:
        return jsonify({'status': 'failed', 'message': 'no data to change'})

    try:
        member = update_member(
            str(member_id),  # UUID to str
            name=data.get('name'),
        )
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'member': member})


@library.route('/library/members/<uuid:member_id>', methods=["DELETE"])
def delete_member_handler(member_id):
    try:
        delete_member(str(member_id))
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'message': 'Member deleted successfully.'})


@library.route('/library/members/<uuid:member_id>/books', methods=['GET'])
def books_borrowed_by_member(member_id):
    try:
        book_ids = get_book_borrowed_by_member(str(member_id))
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})

    return jsonify({'books': book_ids})


# Library Actions

@library.route('/library', methods=['GET'])
def get_borrowed_data_handler():
    borrow_filter = request.args.get('borrow', None)
    if borrow_filter == 'true':
        borrow_filter = True
    elif borrow_filter == 'false':
        borrow_filter = False
    else:
        borrow_filter = None
    return jsonify({'data': borrow_data(borrow_filter)})


@library.route('/library', methods=['POST'])
def borrow_book_handler():
    data = request.json
    if not (data and all([i in data for i in ['isbn', 'member_id']])):
        return jsonify({'status': 'failed', 'message': 'Insufficient data'})

    try:
        borrow_book(data['isbn'], data['member_id'])
    except BookNotFound:
        return jsonify({'status': 'failed', 'message': 'Book Not Found'})
    except MemberNotFound:
        return jsonify({'status': 'failed', 'message': 'Member Not Found'})
    except BookAlreadyTaken:
        return jsonify({'status': 'failed', 'message': 'Book Already Taken'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'message': 'book borrowed'})


@library.route('/library', methods=['PUT'])
def return_borrowed_book_handler():
    data = request.json
    if not (data and all([i in data for i in ['isbn', 'member_id']])):
        return jsonify({'status': 'failed', 'message': 'Insufficient data'})

    try:
        return_book(data['isbn'], data['member_id'])
    except BookNotBorrowed:
        return jsonify({'status': 'failed', 'message': 'book not borrowed'})
    except BadValueError:
        return jsonify({'status': 'failed', 'message': 'Bad Value'})

    return jsonify({'status': 'success', 'message': 'book returned'})
