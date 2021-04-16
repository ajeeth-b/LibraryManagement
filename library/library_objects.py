class Member(object):

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if type(new_name) != str:
            raise TypeError('Name should of string type.')
        if new_name == '':
            raise ValueError('Name cannot be empty.')
        self._name = new_name


class Book(object):

    def __init__(self, name, isbn, author):
        self.name = name
        self.isbn = isbn
        self.author = author

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if type(new_name) != str:
            raise TypeError('Name should of string type.')
        if new_name == '':
            raise ValueError('Name cannot be empty.')
        self._name = new_name

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, val):
        if not (type(val) == str or type(val) == int):
            raise TypeError('ISBN should of integer type.')
        if val == '' or val == 0:
            raise ValueError('ISBN cannot be empty.')
        self._isbn = val

    @property
    def author(self):
        return self._isbn

    @isbn.setter
    def author(self, val):
        if type(val) != str:
            raise TypeError('Author should of string type.')
        if val == '':
            raise ValueError('Name cannot be empty.')
        self._author = val


class MemberManager(object):
    __next_id = 1

    def __init__(self):
        self.members = {}

    def add_member(self, member):
        if type(member) != Member:
            raise TypeError('Objects of type Member is only allowed.')
        self.members[MemberManager.__next_id] = member
        print(f'Member added successfully.\nMember ID is {MemberManager.__next_id}')
        MemberManager.__next_id += 1
        return MemberManager.__next_id-1

    def get_all_member(self):
        return self.members.keys()

    def get_member(self, member_id):
        if member_id not in self.members:
            return None
        return self.members[member_id]

    def delete_member(self, member_id):
        if member_id not in self.members:
            print('Member not found')
        else:
            del self.members[member_id]
            print('Member deleted successfully')


class BookManager(object):
    __next_id = 1

    def __init__(self):
        self.books = {}

    def add_book(self, book):
        if type(book) != Book:
            raise TypeError('Objects of type Books can only be added.')
        self.books[BookManager.__next_id] = book
        print(f'Book added successfully.\nBook ID is {BookManager.__next_id}')
        BookManager.__next_id += 1
        return BookManager.__next_id-1

    def get_all_books(self):
        return self.books.keys()

    def get_book(self, book_id):
        if book_id not in self.books:
            return None
        return self.books[book_id]

    def delete_book(self, book_id):
        if book_id not in self.books:
            print('Book not found')
        else:
            del self.books[book_id]
            print('Book deleted successfully')

    def show_books_except(self, book_id_list):
        return list(set(self.books.keys()) - set(book_id_list))

