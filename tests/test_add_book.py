import pytest
from services.library_service import (
    add_book_to_catalog
)


def test_add_book_valid_input(mocker):
    "Test successfully adding a book"
    title = "Test Book"
    isbn = "1234567890123"

    mocker.patch(
        'services.library_service.get_book_by_isbn',
        return_value=None
    )

    mocker.patch(
        'services.library_service.insert_book',
        return_value=True
    )

    success, message = add_book_to_catalog(title, "Test Author", isbn, 5)

    assert success == True
    assert f'Book "{title}" has been successfully added to the catalog.' in message

def test_add_book_database_erro(mocker):
    "Test getting a dataabase error when adding a book"
    title = "Test Book"
    isbn = "1234567890123"

    mocker.patch(
        'services.library_service.get_book_by_isbn',
        return_value=None
    )

    mocker.patch(
        'services.library_service.insert_book',
        return_value=False
    )

    success, message = add_book_to_catalog(title, "Test Author", isbn, 5)

    assert success == False
    assert "Database error occurred while adding the book." in message
    

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "ISBN must be exactly 13 digits." in message

def test_add_book_negative_copies():
    """Test adding a book with negative copy amount."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890124", -5)
    
    assert success == False
    assert "Total copies must be a positive integer." in message

def test_add_book_no_author():
    """Test adding a book with no author."""
    success, message = add_book_to_catalog("Test Book", "", "1234567890125", 5)
    
    assert success == False
    assert "Author is required." in message    

def test_add_book_already_existing():
    """Test adding a book that already exists."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "9780743273565", 5)
    
    assert success == False
    assert "A book with this ISBN already exists." in message

def test_add_book_no_title():
    """Test adding a book with no title."""
    success, message = add_book_to_catalog("", "Test Author", "1234567890124", 5)
    
    assert success == False
    assert "Title is required." in message

def test_add_book_title_too_long():
    """Test adding a book with 201 characters in the title"""
    success, message = add_book_to_catalog(
        "012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
        "Test Author", 
        "1234567890124", 
        5
        )
    
    assert success == False
    assert "Title must be less than 200 characters." in message

def test_add_book_author_too_long():
    """Test adding a book with an author name containing 105 characters."""
    success, message = add_book_to_catalog("Test Book", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "1234567890124", 5)
    
    assert success == False
    assert "Author must be less than 100 characters." in message


