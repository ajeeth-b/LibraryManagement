from flask import Blueprint, g, redirect, render_template, request
from .authentication import login_required
from .library_manager import get_book_borrowed_by_member, get_book, BookNotFound, MemberNotFound, return_book, BookNotBorrowed, get_all_books, borrow_book

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
@login_required
def index():
	return render_template('index.html')



@user_blueprint.route('/borrow-book', methods=['GET'])
def get_available_book_list():
	return render_template('books.html')

