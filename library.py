class LibrarySystem:
    def __init__(self, users, books):
        self.users = users
        self.books = books
        self.current_user = None

    def login(self, student_id, pin):
        user = self.users.get(student_id)
        if user and user["pin"] == pin:
            self.current_user = student_id
            return True
        return False

    def view_borrowed_books(self):
        return self.users[self.current_user]["borrowed"]

    def borrow_book(self, book_id):
        if book_id not in self.books:
            return "Book not found."
        if not self.books[book_id]["available"]:
            return "Book already borrowed."
        if len(self.users[self.current_user]["borrowed"]) >= 3:
            return "Borrowing limit reached."
        if book_id in self.users[self.current_user]["borrowed"]:
            return "Book already borrowed by user."

        self.books[book_id]["available"] = False
        self.users[self.current_user]["borrowed"].append(book_id)
        return "Book borrowed successfully."

    def return_book(self, book_id):
        if book_id not in self.users[self.current_user]["borrowed"]:
            return "You did not borrow this book."

        self.books[book_id]["available"] = True
        self.users[self.current_user]["borrowed"].remove(book_id)
        return "Book returned successfully."
