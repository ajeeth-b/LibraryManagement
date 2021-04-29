from flask import Blueprint, g, redirect, render_template, request
from .authentication import login_required
from .library_manager import query_book, BookNotFound, MemberNotFound, return_book, BookNotBorrowed, get_all_books, borrow_book

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
@login_required
def index():
	return render_template('index.html')



@user_blueprint.route('/return-book', methods=['POST'])
def user_returns_book():
	book_id = request.form.get('book_id', None)
	if book_id is None:
		return redirect('/')

	if type(book_id) != int:
		if book_id.isdigit():
			book_id = int(book_id)
		else:
			return redirect('/')	

	try:
		return_book(book_id, g.user['member_id'])
	except BookNotBorrowed:
		return redirect('/')
	return redirect('/')


@user_blueprint.route('/borrow-book', methods=['GET'])
def get_available_book_list():
	return render_template('books.html')


@user_blueprint.route('/borrow-book', methods=['POST'])
def user_borrows_book():
	book_id = request.form.get('book_id', None)
	if book_id is None:
		return redirect('/borrow-book')

	if type(book_id) != int:
		if book_id.isdigit():
			book_id = int(book_id)
		else:
			return redirect('/borrow-book')	

	try:
		borrow_book(book_id, g.user['member_id'])
	except BookNotBorrowed:
		return redirect('/')
	except MemberNotFound:
		return redirect('/login')
	return redirect('/')
