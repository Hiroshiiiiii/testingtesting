import unittest
from borrowbooks import BORROWBOOKS
from data import users


class TestBORROWBOOKS(unittest.TestCase):
    def setUp(self):
        self.atm = BORROWBOOKS(users.copy())  # fresh copy for each test

    def test_login_success(self):
        self.assertTrue(self.atm.login("123456", "1234"))

    def test_login_fail(self):
        self.assertFalse(self.atm.login("123456", "0000"))
    
    def test_borrow_book_success(self):
        self.atm.login("123456", "1234")
        result = self.atm.borrow_book("book1")
        self.assertTrue(result)
        self.assertIn("book1", self.atm.get_borrowed_books())
    
    def test_borrow_book_fail(self):
        self.atm.login("123456", "1234")
        result = self.atm.borrow_book("book2")
        self.assertFalse(result)
        self.assertNotIn("book2", self.atm.get_borrowed_books())

    def test_return_book_success(self):