class BORROWBOOKS:
    def __init__(self, book_data):
        self.book_data = book_data
        self.current_user = None
        self.current_book = None
        self.borrowed_books = []

    def login(self, account_number):
        if account_number in self.book_data:
            self.current_user = account_number
            return True
        return False
    
    def borrow_book(self, book_id):
        if self.current_user and book_id in self.book_data:
            book = self.book_data[book_id]
            if book['available']:
                book['available'] = False
                self.borrowed_books.append(book_id)
                return True
        return False
    
    def return_book(self, book_id):
        if self.current_user and book_id in self.borrowed_books:
            book = self.book_data[book_id]
            book['available'] = True
            self.borrowed_books.remove(book_id)
            return True
        
        return False
    def get_borrowed_books(self):
        return self.borrowed_books
    
    def get_book_info(self, book_id):
        if book_id in self.book_data:
            return self.book_data[book_id]
        return None
    
    def get_available_books(self):
        return {book_id: book for book_id, book in self.book_data.items() if book['available']}
    
    def get_user_info(self):
        if self.current_user:
            return self.book_data[self.current_user]
        return None
    
    def logout(self):
        self.current_user = None
        self.borrowed_books = []
        return True
    
    def get_borrowed_books_count(self):
        return len(self.borrowed_books)
    
    def get_book_count(self):
        return len(self.book_data)
    
    def get_available_books_count(self):
        return len(self.get_available_books())
    def get_book_info_by_title(self, title):
        for book_id, book in self.book_data.items():
            if book['title'] == title:
                return book
        return None
    def get_book_info_by_author(self, author):
        for book_id, book in self.book_data.items():
            if book['author'] == author:
                return book
        return None
    def get_book_info_by_genre(self, genre):
        for book_id, book in self.book_data.items():
            if book['genre'] == genre:
                return book
        return None
    def get_book_info_by_year(self, year):
        for book_id, book in self.book_data.items():
            if book['year'] == year:
                return book
        return None

