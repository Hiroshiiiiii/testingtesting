import unittest
from library import LibrarySystem
from data import users, books
from copy import deepcopy


class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.library = LibrarySystem(deepcopy(users), deepcopy(books))
        self.library.login("123456", "1234")

    def test_successful_login(self):
        self.assertTrue(self.library.login("123456", "1234"))

    def test_failed_login(self):
        self.assertFalse(self.library.login("123456", "9999"))

    def test_login_nonexistent_account(self):
        """Test login attempt with a non-existent account."""
        self.assertFalse(self.library.login("000000", "1111"))

    def test_borrow_book_success(self):
        result = self.library.borrow_book("B005")  # Borrow 'Noli Me Tangere'
        self.assertEqual(result, "Book borrowed successfully.")
        self.assertIn("B005", self.library.view_borrowed_books())

    def test_borrow_already_borrowed(self):
        self.library.borrow_book("B006")  # Borrow 'El Filibusterismo'
        result = self.library.borrow_book("B006")  # Try borrowing again
        self.assertEqual(result, "Book already borrowed.")

    def test_borrow_unavailable_book(self):
        """Test borrowing a book that is unavailable."""
        self.library.borrow_book("B007")  # Borrow 'Dekada '70'
        self.library.login("654321", "4321")
        result = self.library.borrow_book("B007")
        self.assertEqual(result, "Book already borrowed.")

    def test_return_book_success(self):
        self.library.borrow_book("B008")  # Borrow 'Smaller and Smaller Circles'
        result = self.library.return_book("B008")
        self.assertEqual(result, "Book returned successfully.")

    def test_return_unborrowed_book(self):
        result = self.library.return_book("B009")  # Try returning 'ABNKKBSNPLAko?!'
        self.assertEqual(result, "You did not borrow this book.")

    def test_borrow_limit(self):
        self.library.borrow_book("B005")  # 'Noli Me Tangere'
        self.library.borrow_book("B006")  # 'El Filibusterismo'
        self.library.borrow_book("B007")  # 'Dekada '70'
        result = self.library.borrow_book("B008")  # 'Smaller and Smaller Circles'
        self.assertEqual(result, "Borrowing limit reached.")

    def test_borrow_nonexistent_book(self):
        result = self.library.borrow_book("B999")  # Non-existent book
        self.assertEqual(result, "Book not found.")

    def test_reborrow_same_book_by_same_user(self):
        self.library.borrow_book("B009")  # Borrow 'ABNKKBSNPLAko?!'
        result = self.library.borrow_book("B009")  # Try borrowing again
        self.assertEqual(result, "Book already borrowed.")

    def test_borrow_after_return(self):
        self.library.borrow_book("B005")  # Borrow 'Noli Me Tangere'
        self.library.return_book("B005")
        result = self.library.borrow_book("B005")  # Borrow again
        self.assertEqual(result, "Book borrowed successfully.")

    def test_borrow_and_return_multiple_users(self):
        """Test borrowing and returning books by multiple users."""
        self.library.borrow_book("B005")  # Borrow 'Noli Me Tangere'
        self.library.borrow_book("B006")  # Borrow 'El Filibusterismo'
        self.library.login("654321", "4321")
        self.assertEqual(
            self.library.borrow_book("B007"),
            "Book borrowed successfully."
        )  # Borrow 'Dekada '70'
        self.assertEqual(
            self.library.return_book("B007"),
            "Book returned successfully."
        )

    def test_return_one_and_borrow_another(self):
        self.library.borrow_book("B005")  # Borrow 'Noli Me Tangere'
        self.library.borrow_book("B006")  # Borrow 'El Filibusterismo'
        self.library.borrow_book("B007")  # Borrow 'Dekada '70'
        self.library.return_book("B006")  # Return 'El Filibusterismo'
        result = self.library.borrow_book("B008")  # Borrow 'Smaller and Smaller Circles'
        self.assertEqual(result, "Book borrowed successfully.")

    def test_view_borrowed_books(self):
        """Test viewing the borrowed books of the current user."""
        self.library.borrow_book("B005")  # 'Noli Me Tangere'
        self.library.borrow_book("B006")  # 'El Filibusterismo'
        borrowed_books = self.library.view_borrowed_books()
        self.assertIn("B005", borrowed_books)
        self.assertIn("B006", borrowed_books)

    def test_borrow_all_books(self):
        """Test borrowing all available books."""
        self.assertEqual(
            self.library.borrow_book("B005"),
            "Book borrowed successfully."
        )  # 'Noli Me Tangere'
        self.assertEqual(
            self.library.borrow_book("B006"),
            "Book borrowed successfully."
        )  # 'El Filibusterismo'
        self.assertEqual(
            self.library.borrow_book("B007"),
            "Book borrowed successfully."
        )  # 'Dekada '70'
        self.assertEqual(
            self.library.borrow_book("B008"),
            "Borrowing limit reached."
        )  # 'Smaller and Smaller Circles'

    def test_return_all_books(self):
        """Test returning all borrowed books."""
        self.library.borrow_book("B005")  # 'Noli Me Tangere'
        self.library.borrow_book("B006")  # 'El Filibusterismo'
        self.library.borrow_book("B007")  # 'Dekada '70'
        self.assertEqual(
            self.library.return_book("B005"),
            "Book returned successfully."
        )
        self.assertEqual(
            self.library.return_book("B006"),
            "Book returned successfully."
        )
        self.assertEqual(
            self.library.return_book("B007"),
            "Book returned successfully."
        )
        borrowed_books = self.library.view_borrowed_books()
        self.assertEqual(len(borrowed_books), 0)


if __name__ == "__main__":
    unittest.main()
