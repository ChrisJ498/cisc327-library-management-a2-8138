import pytest
from services.library_service import (
    get_patron_status_report
)

def test_patron_with_no_books():
    status_report = get_patron_status_report("111111")
    assert status_report["total_books_borrowed"] == 0

def test_patron_calculated_late_fees(mocker):
    fake_books = [
        {"book_id": 1, "title": "Book A"}, 
        {"book_id": 2, "title": "Book B"},
        {"book_id": 3, "title": "Book C"}
    ]

    mocker.patch(
        'services.library_service.get_patron_borrowed_books',
        return_value=fake_books
    )
    
    mocker.patch(
        'services.library_service.get_patron_borrow_count',
        return_value=3
    )

    fake_fees = [
        {'fee_amount': 5.00},
        {'fee_amount': 0.00},
        {'fee_amount': 2.50}
    ]
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        side_effect=fake_fees
    )

    status_report = get_patron_status_report("123456")

    assert status_report["total_late_fees"] == 7.50

