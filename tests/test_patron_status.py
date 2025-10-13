import pytest
from library_service import (
    get_patron_status_report
)

def test_patron_with_books():
    status_report = get_patron_status_report("123456")
    assert status_report["total_books_borrowed"] == 2 #Went to site and borrowed 2 books under patron id 123456

def test_patron_with_invalid_id():
    success, message = get_patron_status_report("abcdefghijk")
    assert success == False
    assert message == "Invalid Patron ID"

def test_patron_with_no_books():
    status_report = get_patron_status_report("111111")
    assert status_report["total_books_borrowed"] == 0



