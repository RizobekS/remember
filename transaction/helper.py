from django.conf import settings
from clickuz import ClickUz
from transaction.models import Transaction
from decimal import Decimal
from rememberApp.views import *
from rememberApp import views


class CheckClickTransaction(ClickUz):
    def check_order(self, order_id: str, amount: str):
        try:
            transaction = Transaction.objects.get(id=int(order_id))
            if transaction.total_price != Decimal(amount):
                return self.INVALID_AMOUNT
            transaction.verify()
        except Transaction.DoesNotExist:
            return 'notfound'
        return self.ORDER_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        try:
            transaction = Transaction.objects.get(id=int(order_id))
            transaction.make_payment()
            payment_type = transaction.transaction_type
            service_id = transaction.service.id
            user = transaction.owner

            return views.payment_success(self, payment_type, service_id, user)

        except Transaction.DoesNotExist:
            return 'not found'
