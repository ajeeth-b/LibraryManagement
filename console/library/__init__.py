from .library import Library


def main():
    library = Library()

    while True:
        print('''
            1. Add book
            2. Add member
            3. Borrow book
            4. Show available book
            5. Return book
            6. Delete book
            7. Delete member
            8. Show all books
            9. Show all members
        ''')

        choice = input('Enter your choice :')
        while not choice.isdigit():
            choice = input('Choice should be an integer:')

        choice = int(choice)

        if choice == 1:
            library.add_book()
        elif choice == 2:
            library.add_member()
        elif choice == 3:
            library.borrow_book()
        elif choice == 4:
            library.show_available_books()
        elif choice == 5:
            library.return_book()
        elif choice == 6:
            library.delete_book()
        elif choice == 7:
            library.delete_member()
        elif choice == 8:
            library.print_all_books()
        elif choice == 9:
            library.print_all_members()
