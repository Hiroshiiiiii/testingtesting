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

    def test_borrow_book_success(self):
        result = self.library.borrow_book("B001")
        self.assertEqual(result, "Book borrowed successfully.")
        self.assertIn("B001", self.library.view_borrowed_books())

    def test_borrow_already_borrowed(self):
        self.library.borrow_book("B001")
        result = self.library.borrow_book("B001")
        self.assertEqual(result, "Book already borrowed.")

    def test_return_book_success(self):
        self.library.borrow_book("B001")
        result = self.library.return_book("B001")
        self.assertEqual(result, "Book returned successfully.")

    def test_return_unborrowed_book(self):
        result = self.library.return_book("B002")
        self.assertEqual(result, "You did not borrow this book.")

    def test_borrow_limit(self):
        self.library.borrow_book("B001")
        self.library.borrow_book("B002")
        self.library.borrow_book("B003")
        result = self.library.borrow_book("B004")
        self.assertEqual(result, "Borrowing limit reached.")

    def test_borrow_nonexistent_book(self):
        result = self.library.borrow_book("B999")
        self.assertEqual(result, "Book not found.")

    def test_reborrow_same_book_by_same_user(self):
        self.library.borrow_book("B001")
        result = self.library.borrow_book("B001")
        self.assertEqual(result, "Book already borrowed.")

    def test_borrow_after_return(self):
        self.library.borrow_book("B001")
        self.library.return_book("B001")
        result = self.library.borrow_book("B001")
        self.assertEqual(result, "Book borrowed successfully.")

    def test_borrow_book_by_another_user(self):
        self.library.borrow_book("B001")
        self.library.login("654321", "4321")
        result = self.library.borrow_book("B001")
        self.assertEqual(result, "Book already borrowed.")

    def test_return_nonexistent_book(self):
        result = self.library.return_book("B999")
        self.assertEqual(result, "You did not borrow this book.")

    def test_return_one_and_borrow_another(self):
        self.library.borrow_book("B001")
        self.library.borrow_book("B002")
        self.library.borrow_book("B003")
        self.library.return_book("B002")
        result = self.library.borrow_book("B004")
        self.assertEqual(result, "Book borrowed successfully.")


if __name__ == "__main__":
    unittest.main()
    