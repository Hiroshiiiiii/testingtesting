class BORROWBOOKS:
    def __init__(self, user_data, book_data):
        self.user_data = user_data
        self.book_data = book_data
        self.current_user = None

    def login(self, student_id, pin):
        if (student_id in self.user_data and
                self.user_data[student_id]["pin"] == pin):
            self.current_user = student_id
            return True
        return False

    def borrow_book(self, book_id):
        if self.current_user is None:
            return False
        if (book_id in self.book_data and
                self.book_data[book_id]["available"]):
            self.user_data[self.current_user]["borrowed_books"].append(book_id)
            self.book_data[book_id]["available"] = False
            return True
        return False

    def return_book(self, book_id):
        if self.current_user is None:
            return False
        if book_id in self.user_data[self.current_user]["borrowed_books"]:
            self.user_data[self.current_user]["borrowed_books"].remove(book_id)
            self.book_data[book_id]["available"] = True
            return True
        return False

    def get_borrowed_books(self):
        if self.current_user is None:
            return []
        return [
            {"book_id": b_id, **self.book_data[b_id]}
            for b_id in self.user_data[self.current_user]["borrowed_books"]
        ]

    def get_available_books(self):
        return [
            {"book_id": b_id, **details}
            for b_id, details in self.book_data.items()
            if details["available"]
        ]

    def search_books(self, title=None, author=None):
        return [
            {"book_id": b_id, **details}
            for b_id, details in self.book_data.items()
            if (title is None or title.lower() in details["title"].lower()) and
               (author is None or author.lower() in details["author"].lower())
        ]

    def logout(self):
        # Logout current user and reset
        self.current_user = None
        return True
