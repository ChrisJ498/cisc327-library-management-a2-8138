import pytest
from library_service import (
    calculate_late_fee_for_book
)

def test_late_fee_on_time():
    """Test book returned before late fee needed"""
    result = calculate_late_fee_for_book("123456", 1)
    
    fee = result['fee_amount']
    days = result['days_overdue']
    status = result['status']

    assert fee == 0.00
    assert days == 0
    assert "not implemented" in status.lower()

def test_late_fee_invalid_patron_id_too_short():
    """Test late fee with patron id too short."""
    result = calculate_late_fee_for_book("1234", 1)
    
    fee = result['fee_amount']
    days = result['days_overdue']
    status = result['status']

    assert fee == 0.00
    assert days == 0
    assert "not implemented" in status.lower()

def test_late_fee_invalid_type_book_id():
    """Test late fee with letters in book id."""
    result = calculate_late_fee_for_book("123456", "abc")
    
    fee = result['fee_amount']
    days = result['days_overdue']
    status = result['status']

    assert fee == 0.00
    assert days == 0
    assert "not implemented" in status.lower()

def test_late_fee_no_patron_id():
    """Test late fee with letters in patron id."""
    result = calculate_late_fee_for_book("", 1)
    
    fee = result['fee_amount']
    days = result['days_overdue']
    status = result['status']

    assert fee == 0.00
    assert days == 0
    assert "not implemented" in status.lower()
