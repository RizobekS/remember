
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from transaction import serializers
from transaction.service import initialize_transaction
from transaction import models
from transaction import helper
from clickuz import ClickUz
from clickuz.views import ClickUzMerchantAPIView
from payme.views import MerchantAPIView

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


class InitializePaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.JWTAuthentication]
    serializer_class = serializers.InitializePaymentSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        transaction_type = data.validated_data.get("transaction_type")
        price = data.validated_data.get("price")

        transaction_id = initialize_transaction(
            request.user,
            price,
            transaction_type,
        )

        generated_link = ""

        if transaction_type == models.TRANSACTIONTYPECHOICES.CLICK:
            price = price * converter_amount_click

            generated_link = ClickUz.generate_url(
                order_id=transaction_id,
                amount=price,
                return_url='http://www.remember.uz/dashboard/'
            )
        elif transaction_type == models.TRANSACTIONTYPECHOICES.VISA:
            pass

        return Response(
            status=status.HTTP_200_OK,
            data={"generated_link": generated_link}
        )


initialize_payment_api_view = InitializePaymentAPIView.as_view()


class AcceptClickRequestsView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = helper.CheckClickTransaction


accept_click_request_view = AcceptClickRequestsView.as_view()
