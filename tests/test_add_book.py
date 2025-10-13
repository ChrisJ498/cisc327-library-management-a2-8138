import pytest
from library_service import (
    add_book_to_catalog
)

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message

def test_add_book_negative_copies():
    """Test adding a book with negative copy amount."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890124", -5)
    
    assert success == False
    assert "need positive integer" in message

def test_add_book_no_author():
    """Test adding a book with no author."""
    success, message = add_book_to_catalog("Test Book", "", "1234567890125", 5)
    
    assert success == False
    assert "need author" in message    

def test_add_book_letters_in_isbn():
    """Test adding a book with ISBN being 13 letters."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "abcdefghijklm", 5)
    
    assert success == False
    assert "invalid isbn" in message