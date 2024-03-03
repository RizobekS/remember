from pyclick import PyClick
from pyclick.views import PyClickMerchantAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from transaction import serializers
from transaction.models import Transaction
from transaction.service import initialize_transaction
from transaction import models
from transaction import helper
from clickuz import ClickUz
from clickuz.views import ClickUzMerchantAPIView
from payme.views import MerchantAPIView
from rememberApp.models import MyTransaction
from remember_project import settings

converter_amount = settings.PAYME_PRICE_HELPER
converter_amount_click = settings.CLICK_PRICE_HELPER


# from rest_framework_simplejwt import authentication


class PaymeCallBackAPIView(MerchantAPIView):
    def create_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"create_transaction for order_id: {order_id}, response: {action}")

    def perform_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"perform_transaction for order_id: {order_id}, response: {action}")

    def cancel_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"cancel_transaction for order_id: {order_id}, response: {action}")


class OrderCheckAndPayment(PyClick):
    def check_order(self, order_id: str, amount: str):
        if order_id:
            try:
                order = Transaction.objects.get(id=order_id)
                if int(amount) == order.amount:
                    return self.ORDER_FOUND
                else:
                    return self.INVALID_AMOUNT
            except Transaction.DoesNotExist:
                return self.ORDER_NOT_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        try:
            order = MyTransaction.objects.get(id=order_id)
            order.status = "paid"
            order.save()
        except Transaction.DoesNotExist:
            print(f"no order object not found: {order_id}")


class AcceptClickRequestsView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = helper.CheckClickTransaction


accept_click_request_view = AcceptClickRequestsView.as_view()


class OrderTestView(PyClickMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment
