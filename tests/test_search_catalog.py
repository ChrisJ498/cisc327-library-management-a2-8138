import pytest
from services.library_service import (
    search_books_in_catalog
)

def test_search_isbn():
    results = search_books_in_catalog("9780743273565", "isbn")
    assert len(results) == 1

def test_search_title_partial():
    results = search_books_in_catalog("Great", "title")
    assert len(results) > 0

def test_search_author_partial():
    results = search_books_in_catalog("harp", "author")
    assert len (results) > 0

def test_not_existing_title():
    results = search_books_in_catalog("12345", "title")
    assert len (results) == 0

