import pytest
from unittest.mock import Mock
from services.library_service import pay_late_fees
from services.payment_service import PaymentGateway

valid_Patron_ID = "123456"
valid_Book_ID = 1
book_Info = {"id": 1, "title": "The Great Gatsby"}

def test_pay_late_fees_success(mocker):
    "Testing for a successful payment of late fees"
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 5.00}
    )

    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value=book_Info
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (
        True, "txn_123", "Payment processed"
    )

    success, message, txn_id = pay_late_fees(
        valid_Patron_ID, valid_Book_ID, mock_gateway
    )

    assert success == True
    assert message == "Payment successful! Payment processed"
    assert txn_id == "txn_123"

    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with(
        patron_id=valid_Patron_ID,
        amount=5.00,
        description="Late fees for 'The Great Gatsby'"
    )

def test_pay_late_fees_declined_by_gateway(mocker):
    "Test for payment declined by gateway"
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 5.00}
    )

    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value=book_Info
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (
        False, None, "Card declined"
    )

    success, message, txn_id = pay_late_fees(
        valid_Patron_ID, valid_Book_ID, mock_gateway
    )

    assert success == False
    assert message == "Payment failed: Card declined"
    assert txn_id == None

    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with(
        patron_id=valid_Patron_ID,
        amount=5.00,
        description="Late fees for 'The Great Gatsby'"
    )

def test_pay_late_fees_invalid_patron_ID():
    "Testing when the patron's ID is invalid, in this case it is too short"
    mock_gateway = Mock(spec=PaymentGateway)
    invalid_patron_id = "123"

    success, message, txn_id = pay_late_fees(
        invalid_patron_id, valid_Book_ID, mock_gateway
    )

    assert success == False
    assert message == "Invalid patron ID. Must be exactly 6 digits."
    assert txn_id == None

    mock_gateway.process_payment.assert_not_called()

def test_pay_late_fees_zero_late_fees(mocker):
    "Testing when the late fees are zero"
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 0.00}
    )

    mock_gateway = Mock(spec=PaymentGateway)

    success, message, txn_id = pay_late_fees(
        valid_Patron_ID, valid_Book_ID, mock_gateway
    )

    assert success == False
    assert message == "No late fees to pay for this book."
    assert txn_id == None
    
    mock_gateway.process_payment.assert_not_called()

def test_pay_late_fees_network_error_exception(mocker):
    "Testing when there is a network error exception handling"
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 5.00}
    )

    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value=book_Info
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("Network error")

    success, message, txn_id = pay_late_fees(
        valid_Patron_ID, valid_Book_ID, mock_gateway
    )

    assert success == False
    assert message == "Payment processing error: Network error"
    assert txn_id == None

    mock_gateway.process_payment.assert_called_once()






        