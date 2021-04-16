from .library_objects import Book, Member, BookManager, MemberManager
from .decorators import enclose_with_hash


class LibraryManager(object):

    def __init__(self):
        self.books = BookManager()
        self.members = MemberManager()

        self.books_taken = []

    # Book operations

    def add_book(self, name, isbn, author):

        book = Book(name, isbn, author)
        self.books.add_book(book)
        return True

    @enclose_with_hash
    def print_all_books(self):
        self.show_book_list_detail(self.books.get_all_books())
        return True

    @enclose_with_hash
    def delete_book(self, book_id):

        if type(book_id) != int:
            raise TypeError('ID should be of integer type')

        if book_id in [i[0] for i in self.books_taken]:
            print('Book is with member, cannot be deleted.')
            return False
        self.books.delete_book(book_id)
        return True

    def show_book_detail(self, book_id):

        if type(book_id) != int:
            raise TypeError('ID should be of integer type')

        book = self.books.get_book(book_id)
        if book is None:
            print(book_id, 'Book data deleted or no such book')
            return False
        print(book_id, book.name, book.isbn, book.author)
        return True

    def show_book_list_detail(self, book_list):
        for i in book_list:
            self.show_book_detail(i)
        return True

    # Member operations

    def add_member(self, name):

        member = Member(name)
        self.members.add_member(member)
        return True

    @enclose_with_hash
    def print_all_members(self):

        for member_id in self.members.get_all_member():
            member = self.members.get_member(member_id)
            if member is None:
                print(member_id, 'member might be deleted.')
            else:
                print(member_id, member.name)
        return True

    def get_member_books(self, member_id):

        if type(member_id) != int:
            raise TypeError('ID should be of integer type')

        member_books = []
        for book_id, l_member_id in self.books_taken:
            if l_member_id == member_id:
                member_books += [book_id]
        return member_books

    @enclose_with_hash
    def delete_member(self, member_id):

        if type(member_id) != int:
            raise TypeError('ID should be of integer type')

        if self.get_member_books(member_id):
            print('Member cannot be deleted without returning books')
            return False

        self.members.delete_member(member_id)
        return True

    # Library operations

    @enclose_with_hash
    def borrow_book(self, member_id, book_id):

        if type(member_id) != int:
            raise TypeError('ID should be of integer type')
        if type(book_id) != int:
            raise TypeError('ID should be of integer type')

        # raise ZeroDivisionError

        member = self.members.get_member(member_id)
        # raise ZeroDivisionError
        if member is None:
            print('Invalid member ID')
            return False
        # raise ZeroDivisionError

        book = self.books.get_book(book_id)
        if not book:
            print('Invalid book ID')
            return False

        if book_id in self.get_available_books():
            print('Book is already taken.')
            return False

        self.books_taken += [(book_id, member_id)]
        print('Success')
        return True

    def delete_entry(self, member_id, book_id):

        if type(member_id) != int:
            raise TypeError('ID should be of integer type')
        if type(book_id) != int:
            raise TypeError('ID should be of integer type')

        index = self.books_taken.index((book_id, member_id))
        del self.books_taken[index]
        return True

    @enclose_with_hash
    def return_book(self, member_id, book_id):

        if type(member_id) != int:
            raise TypeError('ID should be of integer type')
        if type(book_id) != int:
            raise TypeError('ID should be of integer type')

        member_books = self.get_member_books(member_id)
        if not member_books:
            print('This member doesnot borrowed any book.')
            return False

        if book_id not in member_books:
            print('No such book taken by the member')
            return False

        self.delete_entry(member_id, book_id)
        print('Book returned successfully.')
        return True

    def get_available_books(self):
        return [i[0] for i in self.books_taken]

    @enclose_with_hash
    def show_available_books(self):
        books_taken = self.get_available_books()
        books_not_taken = self.books.show_books_except(books_taken)
        self.show_book_list_detail(books_not_taken)
        return True


# Overriding classes for input from console

class Library(LibraryManager):
    def __init__(self):
        super(Library, self).__init__()

    @enclose_with_hash
    def add_book(self):
        name = input('Enter the book name    :')
        while not name:
            name = input('Name cannot be empty   :')
        isbn = input('Enter the ISBN number  :')
        while not isbn:
            isbn = input('ISBN cannot be empty   :')
        author = input('Enter the author name  :')
        while not author:
            author = input('Author name cannot be empty:')

        book = Book(name, isbn, author)
        self.books.add_book(book)

    @enclose_with_hash
    def delete_book(self):
        book_id = input('Enter the book ID  :')
        while not book_id.isdigit():
            book_id = input('The book ID must be in integer :')
        book_id = int(book_id)

        if book_id in [i[0] for i in self.books_taken]:
            print('Book is with member, cannot be deleted.')
            return
        self.books.delete_book(book_id)

    @enclose_with_hash
    def add_member(self):
        name = input('Enter the member name :')
        while not name:
            name = input('Name cannot be empty')

        member = Member(name)
        self.members.add_member(member)

    @enclose_with_hash
    def delete_member(self):
        member_id = input('Enter the member ID  :')
        while not member_id.isdigit():
            member_id = input('The member ID must be in integer :')

        member_id = int(member_id)
        if self.get_member_books(member_id):
            print('Member cannot be deleted without returning books')
            return

        self.members.delete_member(member_id)

    # Library operations

    @enclose_with_hash
    def borrow_book(self):
        member_id = input('Enter the member ID  :')
        while not member_id.isdigit():
            member_id = input('The member ID must be in integer :')

        member_id = int(member_id)
        member = self.members.get_member(member_id)
        if member is None:
            print('Invalid member ID')
            return

        book_id = input('Enter the book ID  :')
        while not book_id.isdigit():
            book_id = input('The book ID must be in integer :')

        book_id = int(book_id)
        book = self.books.get_book(book_id)
        if not book:
            print('Invalid book ID')
            return

        if book_id in self.get_available_books():
            print('Book is already taken.')
            return

        self.books_taken += [(book_id, member_id)]
        print('Success')

    @enclose_with_hash
    def return_book(self):
        member_id = input('Enter the member ID  :')
        while not member_id.isdigit():
            member_id = input('The member ID must be in integer :')

        member_id = int(member_id)
        member_books = self.get_member_books(member_id)
        if not member_books:
            print('This member doesnot borrowed any book.')
            return

        print('There are the books taken by user.\nEnter id from the following')
        self.show_book_list_detail(member_books)

        book_id = input('Enter the book ID')
        book_id = int(book_id)
        if book_id not in member_books:
            print('No such book taken by the member')
            return

        self.delete_entry(member_id, book_id)
        print('Book returned successfully.')
