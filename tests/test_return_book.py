import pytest
from library_service import (
    return_book_by_patron
)

def test_return_book_valid_input():
    """Test returning a book with valid input."""
    success, message = return_book_by_patron("123456", 1)
    
    assert success == True
    assert "successfully return" in message.lower()

def test_return_book_invalid_patron_id_too_short():
    """Test returning a book with patron id too short."""
    success, message = return_book_by_patron("1234", 1)
    
    assert success == False
    assert "need 6 digit patron id" in message.lower

def test_return_book_invalid_type_book_id():
    """Test returning a book with letters in book id."""
    success, message = return_book_by_patron("123456", "abc")
    
    assert success == False
    assert "invalid book id" in message.lower()

def test_return_book_invalid_type_patron_id():
    """Test returning a book with letters in patron id."""
    success, message = return_book_by_patron("abcdef", 1)
    
    assert success == False
    assert "invalid patron id" in message.lower()

def test_return_book_negative_book_id():
    """Test returning a book with negative book id."""
    success, message = return_book_by_patron("123456", -1)
    
    assert success == False
    assert "invalid book id" in message.lower()