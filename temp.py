from library.library import LibraryManager

l = LibraryManager()

l.add_book('name', 'isbn', 'author')
l.add_member('aj')

l.borrow_book(1, 1)
l.return_book(1, 1)
l.delete_book(1)
l.get_available_books()
l.print_all_books()
l.print_all_members()