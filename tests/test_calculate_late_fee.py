import pytest
from datetime import datetime, timedelta
from services.library_service import calculate_late_fee_for_book


def test_late_fee_on_time(mocker):
    "Test book returned on time"
    due_date = datetime.now()

    fake_borrowed_book = [
        {"book_id": 1, "due_date": due_date}
    ]

    mocker.patch(
        'services.library_service.get_patron_borrowed_books',
        return_value=fake_borrowed_book
    )

    result = calculate_late_fee_for_book(123456, 1)

    assert result['fee_amount'] == 0.00
    assert result['days_overdue'] == 0
    assert result['status'] == "Late fee calculated"

def test_late_fee_under_7_days(mocker):
    "Tests late fee when under 7 days late"
    due_date = datetime.now() - timedelta(days=5)
    
    fake_borrowed_book = [
        {"book_id": 1, "due_date": due_date}
    ]

    mocker.patch(
        'services.library_service.get_patron_borrowed_books',
        return_value=fake_borrowed_book
    )

    result = calculate_late_fee_for_book(123456, 1)

    assert result['fee_amount'] == 2.50
    assert result['days_overdue'] == 5
    assert result['status'] == "Late fee calculated"

def test_late_fee_over_7_days(mocker):
    """Tests for when the book is more than 7 dyas overdue"""
    due_date = datetime.now() - timedelta(days=10)
    
    fake_borrowed_book = [
        {"book_id": 1, "due_date": due_date}
    ]
    mocker.patch(
        'services.library_service.get_patron_borrowed_books',
        return_value=fake_borrowed_book
    )
    
    result = calculate_late_fee_for_book(123456, 1)

    assert result['fee_amount'] == 6.50
    assert result['days_overdue'] == 10
    assert result['status'] == "Late fee calculated"   

def test_calculate_late_fee_max_cap(mocker):
    """Tests for when late fee caps out at $15"""
    due_date = datetime.now() - timedelta(days=30)
    
    fake_borrowed_book = [
        {"book_id": 1, "due_date": due_date}
    ]
    mocker.patch(
        'services.library_service.get_patron_borrowed_books',
        return_value=fake_borrowed_book
    )
    
    result = calculate_late_fee_for_book(123456, 1)

    assert result['fee_amount'] == 15.00
    assert result['days_overdue'] == 30
    assert result['status'] == "Late fee calculated"    




