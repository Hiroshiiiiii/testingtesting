import unittest
from borrowbooks import BORROWBOOKS
from data import users, books


class TestBORROWBOOKS(unittest.TestCase):
    def setUp(self):
        # Initialize BORROWBOOKS with a fresh copy of user and book data before each test
        self.library = BORROWBOOKS(users.copy(), books.copy())

    # Test successful login
    def test_login_success(self):
        self.assertTrue(self.library.login("raejohn", "1234"))
        self.assertEqual(self.library.current_user, "raejohn")

    # Test failed login due to incorrect PIN
    def test_login_fail_wrong_pin(self):
        self.assertFalse(self.library.login("raejohn", "0000"))
        self.assertIsNone(self.library.current_user)

    # Test failed login due to non-existent user
    def test_login_fail_nonexistent_user(self):
        self.assertFalse(self.library.login("nonexistent_user", "1234"))
        self.assertIsNone(self.library.current_user)

    # Test borrowing a book successfully
    def test_borrow_book_success(self):
        self.library.login("raejohn", "1234")
        result = self.library.borrow_book("book1")
        self.assertTrue(result)
        self.assertIn("book1", self.library.user_data["raejohn"]["borrowed_books"])
        self.assertFalse(self.library.book_data["book1"]["available"])

    # Test borrowing a book that is already borrowed (unavailable)
    def test_borrow_book_fail_unavailable(self):
        self.library.login("raejohn", "1234")
        self.library.borrow_book("book1")
        self.library.logout()

        self.library.login("regie", "4321")
        result = self.library.borrow_book("book1")
        self.assertFalse(result)
        self.assertNotIn("book1", self.library.user_data["regie"]["borrowed_books"])

    # Test borrowing a book without being logged in
    def test_borrow_book_fail_not_logged_in(self):
        result = self.library.borrow_book("book1")
        self.assertFalse(result)

    # Test returning a book successfully
    def test_return_book_success(self):
        self.library.login("raejohn", "1234")
        self.library.borrow_book("book1")
        result = self.library.return_book("book1")
        self.assertTrue(result)
        self.assertNotIn("book1", self.library.user_data["raejohn"]["borrowed_books"])
        self.assertTrue(self.library.book_data["book1"]["available"])

    # Test returning a book that was not borrowed
    def test_return_book_fail_unborrowed(self):
        self.library.login("jericho", "5678")
        result = self.library.return_book("book2")
        self.assertFalse(result)

    # Test returning a book without being logged in
    def test_return_book_fail_not_logged_in(self):
        result = self.library.return_book("book1")
        self.assertFalse(result)

    # Test retrieving a list of borrowed books
    def test_get_borrowed_books(self):
        self.library.login("jericho", "5678")
        self.library.borrow_book("book1")
        self.library.borrow_book("book2")
        borrowed_books = self.library.get_borrowed_books()
        self.assertEqual(len(borrowed_books), 2)
        self.assertIn("book1", [book["book_id"] for book in borrowed_books])
        self.assertIn("book2", [book["book_id"] for book in borrowed_books])

    # Test retrieving an empty list of borrowed books
    def test_get_borrowed_books_empty(self):
        self.library.login("jericho", "5678")
        borrowed_books = self.library.get_borrowed_books()
        self.assertEqual(len(borrowed_books), 0)

    # Test getting a list of available books
    def test_get_available_books(self):
        self.library.login("jericho", "5678")
        self.library.borrow_book("book1")
        available_books = self.library.get_available_books()
        self.assertNotIn("book1", available_books)
        self.assertIn("book2", available_books)

    # Test searching books by title
    def test_search_books_by_title(self):
        results = self.library.search_books(title="1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "1984")

    # Test searching books by author
    def test_search_books_by_author(self):
        results = self.library.search_books(author="J.R.R. Tolkien")
        self.assertEqual(len(results), 2)
        self.assertIn("The Lord of the Rings", [book["title"] for book in results])
        self.assertIn("The Hobbit", [book["title"] for book in results])

    # Test searching books with no results
    def test_search_books_no_results(self):
        results = self.library.search_books(title="Nonexistent Book")
        self.assertEqual(len(results), 0)

    # Test logging out
    def test_logout(self):
        self.library.login("jericho", "5678")
        self.library.logout()
        self.assertIsNone(self.library.current_user)

    # Test that two users can borrow different books independently
    def test_borrow_book_multiple_users(self):
        self.library.login("raejohn", "1234")
        self.library.borrow_book("book1")
        self.library.logout()

        self.library.login("regie", "4321")
        result = self.library.borrow_book("book2")
        self.assertTrue(result)
        self.assertIn("book2", self.library.user_data["regie"]["borrowed_books"])

    # Test that only the user who borrowed a book can return it
    def test_return_book_multiple_users(self):
        self.library.login("raejohn", "1234")
        self.library.borrow_book("book1")
        self.library.logout()

        self.library.login("regie", "4321")
        result = self.library.return_book("book1")
        self.assertFalse(result)

        self.library.login("raejohn", "1234")
        result = self.library.return_book("book1")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
