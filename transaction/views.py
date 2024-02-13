from django.conf import settings
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response


from clickuz import ClickUz
from clickuz.views import ClickUzMerchantAPIView
from payme.views import MerchantAPIView

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


#class AcceptClickRequestsView(ClickUzMerchantAPIView):
    #VALIDATE_CLASS = helper.CheckClickTransaction


#accept_click_request_view = AcceptClickRequestsView.as_view()

