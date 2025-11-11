import pytest
from services.payment_service import PaymentGateway

valid_patron_id = "123456"
valid_amount = 10.50
valid_txn_id = "txn_123456"

def test_process_payment_success():
    "Test for successful payment"
    gateway = PaymentGateway()

    success, transaction_id, message = gateway.process_payment(
        patron_id=valid_patron_id,
        amount=valid_amount,
        description="Late fees"
    )

    assert success == True
    assert transaction_id.startswith(f"txn_{valid_patron_id}_")
    assert message == f"Payment of ${valid_amount:.2f} processed successfully"

def test_process_payment_invalid_amount_zero():
    "Test for invalid amount (needs to be greater than 0), 0 in this case"
    gateway = PaymentGateway()
    
    success, transaction_id, message = gateway.process_payment(
        patron_id=valid_patron_id,
        amount=0.00,
        description="Late fees"
    )
    
    assert success == False
    assert transaction_id == ""
    assert message == "Invalid amount: must be greater than 0"

def test_process_payment_invalid_amount_negative():
    "Test for invalid amount (needs to be greater than 0), negative in this case, specifically -5"
    gateway = PaymentGateway()
    
    success, transaction_id, message = gateway.process_payment(
        patron_id=valid_patron_id,
        amount=-5.00,
        description="Late fees"
    )
    
    assert success == False
    assert transaction_id == ""
    assert message == "Invalid amount: must be greater than 0"

def test_process_payment_exceeds_limit():
    "Tests for when the payment limit is exceeded (greater than 1000), 1001.00 in this case"
    gateway = PaymentGateway()
    
    success, transaction_id, message = gateway.process_payment(
        patron_id=valid_patron_id,
        amount=1001.00,
        description="Late fees"
    )
    
    assert success == False
    assert transaction_id == ""
    assert message == "Payment declined: amount exceeds limit"

def test_process_payment_invalid_patron_id_format():
    "Tests fpr an invalid format of the patron ID. Too short in this case"
    gateway = PaymentGateway()
    
    success, transaction_id, message = gateway.process_payment(
        patron_id="12345",
        amount=valid_amount,
        description="Late fees"
    )
    
    assert success == False
    assert transaction_id == ""
    assert message == "Invalid patron ID format"

def test_refund_payment_success():
    "Tests for a successful refund payment"
    gateway = PaymentGateway()
    
    success, message = gateway.refund_payment(
        transaction_id=valid_txn_id,
        amount=valid_amount
    )
    
    assert success == True
    assert message.startswith(f"Refund of ${valid_amount:.2f} processed successfully.")
    assert "Refund ID: refund_txn_123456_" in message

def test_refund_payment_invalid_transaction_id():
    "Tests for an invalid transaction ID. Ie, does not start with txn_"
    gateway = PaymentGateway()
    
    success, message = gateway.refund_payment(
        transaction_id="not_valid",
        amount=valid_amount
    )
    
    assert success == False
    assert message == "Invalid transaction ID"

def test_refund_payment_invalid_amount_zero():
    "Tests for an invalid refund amount. This case being zero"
    gateway = PaymentGateway()
    
    success, message = gateway.refund_payment(
        transaction_id=valid_txn_id,
        amount=0.00
    )
    
    assert success == False
    assert message == "Invalid refund amount"

def test_refund_payment_invalid_amount_negative():
    "Tests for an invalid refund amount. This case being negative"
    gateway = PaymentGateway()
    
    success, message = gateway.refund_payment(
        transaction_id=valid_txn_id,
        amount=-5.00
    )
    
    assert success == False
    assert message == "Invalid refund amount"