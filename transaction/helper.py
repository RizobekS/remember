from django.conf import settings
from paycomuz import Paycom
from clickuz import ClickUz
from transaction.models import Transaction
from transaction import service
from decimal import Decimal
from rememberApp.views import *
from rememberApp import views
converter_amount = settings.PAYME_PRICE_HELPER


class CheckPayMeTransaction(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(id=account['order_id'])

            if transaction.total_price != amount / converter_amount:
                return self.INVALID_AMOUNT
            transaction.verify()
        except Transaction.DoesNotExist:
            return self.ORDER_NOT_FOND
        return self.ORDER_FOUND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        service.pay_transaction(transaction.order_key)

        transaction = Transaction.objects.get(id=int(transaction.order_key))
        transaction.make_payment()
        payment_type = transaction.transaction_type
        tour_id = transaction.tour.id
        user = transaction.owner

        return views.payment_success(self, payment_type, tour_id, user)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        service.cancel_transaction(transaction.order_key)


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
            tour_id = transaction.tour.id
            user = transaction.owner

            return views.payment_success(self, payment_type, tour_id, user)

        except Transaction.DoesNotExist:
            return 'not found'