from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity
        self.checked_out = []

    def is_available(self):
        return self.quantity > len(self.checked_out)

    def checkout(self, user_id):
        if self.is_available():
            self.checked_out.append((user_id, datetime.now()))
            return True
        else:
            return False

    def return_book(self, user_id):
        for index, (uid, checkout_date) in enumerate(self.checked_out):
            if uid == user_id:
                self.checked_out.pop(index)
                return checkout_date
        return None

    def calculate_fine(self, checkout_date):
        due_date = checkout_date + timedelta(days=14)
        if datetime.now() > due_date:
            overdue_days = (datetime.now() - due_date).days
            return overdue_days
        else:
            return 0

class Library:
    def __init__(self):
        self.catalog = {}

    def add_book(self, book_id, title, author, quantity):
        self.catalog[book_id] = Book(book_id, title, author, quantity)

    def display_catalog(self):
        for book_id, book in self.catalog.items():
            availability = "Available" if book.is_available() else "Not Available"
            print(f"ID: {book_id}, Title: {book.title}, Author: {book.author}, Availability: {availability}")

    def checkout_book(self, book_id, user_id):
        if book_id in self.catalog:
            if self.catalog[book_id].checkout(user_id):
                print("Book checked out successfully.")
            else:
                print("Book is not available for checkout.")
        else:
            print("Book not found in catalog.")

    def return_book(self, book_id, user_id):
        if book_id in self.catalog:
            checkout_date = self.catalog[book_id].return_book(user_id)
            if checkout_date:
                fine = self.catalog[book_id].calculate_fine(checkout_date)
                if fine > 0:
                    print(f"Book returned successfully. Overdue fine: ${fine}")
                else:
                    print("Book returned successfully.")
            else:
                print("You have not checked out this book.")
        else:
            print("Book not found in catalog.")

    def list_overdue_books(self, user_id):
        overdue_books = []
        total_fine = 0
        for book_id, book in self.catalog.items():
            for uid, checkout_date in book.checked_out:
                if uid == user_id:
                    fine = book.calculate_fine(checkout_date)
                    if fine > 0:
                        overdue_books.append((book_id, book.title, fine))
                        total_fine += fine
        if overdue_books:
            print("Overdue Books:")
            for book_id, title, fine in overdue_books:
                print(f"ID: {book_id}, Title: {title}, Fine: ${fine}")
            print(f"Total Fine: ${total_fine}")
        else:
            print("No overdue books.")

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class LibrarySystem:
    def __init__(self):
        self.library = Library()
        self.users = {}

    def register_user(self, user_id, name):
        if user_id not in self.users:
            self.users[user_id] = User(user_id, name)
            print("User registered successfully.")
        else:
            print("User ID already exists.")

    def display_catalog(self):
        self.library.display_catalog()

    def checkout_book(self, book_id, user_id):
        self.library.checkout_book(book_id, user_id)

    def return_book(self, book_id, user_id):
        self.library.return_book(book_id, user_id)

    def list_overdue_books(self, user_id):
        self.library.list_overdue_books(user_id)

# Sample usage:
library_system = LibrarySystem()
library_system.register_user("U001", "Alice")
library_system.register_user("U002", "Bob")

library_system.library.add_book("B001", "Python Programming", "John Smith", 3)
library_system.library.add_book("B002", "Data Structures", "Jane Doe", 2)

library_system.display_catalog()

library_system.checkout_book("B001", "U001")
library_system.checkout_book("B001", "U002")  # This should fail due to limit
library_system.checkout_book("B002", "U001")

library_system.return_book("B001", "U001")
library_system.return_book("B001", "U001")  # This should fail as book is not checked out by this user
library_system.return_book("B002", "U001")

library_system.list_overdue_books("U001")
library_system.list_overdue_books("U002")
