import pytest
from library_service import (
    borrow_book_by_patron
)

def test_borrow_book_valid_input():
    """Test borrowing a book with valid input."""
    success, message = borrow_book_by_patron("123456", 1)
    
    assert success == True
    assert "successfully borrowed" in message.lower()

def test_borrow_book_invalid_patron_id_too_short():
    """Test borrowing a book with patron id too short."""
    success, message = borrow_book_by_patron("1234", 1)
    
    assert success == False
    assert "need 6 digit patron id" in message.lower

def test_borrow_book_invalid_type_book_id():
    """Test borrowing a book with letters in book id."""
    success, message = borrow_book_by_patron("123456", "abc")
    
    assert success == False
    assert "invalid book id" in message.lower()

def test_borrow_book_invalid_type_patron_id():
    """Test borrowing a book with letters in patron id."""
    success, message = borrow_book_by_patron("abcdef", 1)
    
    assert success == False
    assert "invalid patron id" in message.lower()

def test_borrow_book_negative_book_id():
    """Test borrowing a book with negative book id."""
    success, message = borrow_book_by_patron("123456", -1)
    
    assert success == False
    assert "invalid book id" in message.lower()