from transaction.models import Transaction
from rememberApp.models import *
from transaction import models


def initialize_transaction(owner, price, transaction_type):
    obj = Transaction.objects.create(
        owner=owner,
        total_price=price,
        transaction_type=transaction_type,
    )

    return obj.id


def initalize_transaction_click(owner, price, service_id):
    service = Services.objects.get(id=service_id)
    obj = Transaction.objects.create(
        owner=owner,
        total_price=price,
        transaction_type=models.TRANSACTIONTYPECHOICES.CLICK,
        service=service
    )
    return obj.id


def initalize_transaction_payme(owner, price, service_id):
    service = Services.objects.get(id=service_id)
    obj = Transaction.objects.create(
        owner=owner,
        total_price=price,
        transaction_type=models.TRANSACTIONTYPECHOICES.PAYME,
        service=service
    )
    return obj.id


def pay_transaction(transaction_id):
    try:
        instance = Transaction.objects.get(id=transaction_id)
        instance.make_payment()
    except Transaction.DoesNotExist:
        return


def cancel_transaction(transaction_id):
    try:
        instance = Transaction.objects.get(id=transaction_id)
        instance.cancel()
    except Transaction.DoesNotExist:
        return
