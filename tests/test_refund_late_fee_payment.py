import pytest
from unittest.mock import Mock
from services.library_service import refund_late_fee_payment
from services.payment_service import PaymentGateway

valid_txn_id = "txn_123"

def test_refund_late_fee_payment_success():
    " Testing when the late fee is refunded successfully"
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (
        True, "Refund of $10.00 processed."
    )

    success, message = refund_late_fee_payment(
        valid_txn_id, 10.00, mock_gateway
    )

    assert success == True
    assert message == "Refund of $10.00 processed."

    mock_gateway.refund_payment.assert_called_once()
    mock_gateway.refund_payment.assert_called_with(valid_txn_id, 10.00)

def test_refund_late_fee_invalid_transaction_id():
    "Testing when there is a refund rejection from an invalid transaction ID"
    mock_gateway = Mock(spec=PaymentGateway)
    invalid_txn_id = "abc"

    success, message = refund_late_fee_payment(
        invalid_txn_id, 10.00, mock_gateway
    )

    assert success == False
    assert message == "Invalid transaction ID."

    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_invalid_amount_zero():
    "Testing when the refund amount is the invalid amount of zero"
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment(
        valid_txn_id, 0.00, mock_gateway
    )

    assert success == False
    assert message == "Refund amount must be greater than 0."

    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_invalid_amount_negative():
    "Testing when the refund amount is the invalid amount of a negative value"
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment(
        valid_txn_id, -5.00, mock_gateway
    )

    assert success == False
    assert message == "Refund amount must be greater than 0."

    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_invalid_amount_exceeds_maximum():
    "Testing when the refund amount is the invalid amount of exceeding the $15 maximum"
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment(
        valid_txn_id, 16.00, mock_gateway
    )

    assert success == False
    assert message == "Refund amount exceeds maximum late fee."

    mock_gateway.refund_payment.assert_not_called()

