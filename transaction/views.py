from django.conf import settings
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from paycomuz import Paycom
from paycomuz.views import MerchantAPIView
from clickuz import ClickUz
from clickuz.views import ClickUzMerchantAPIView
from transaction import serializers
from transaction import models
from transaction import helper

from transaction.service import initialize_transaction

converter_amount = settings.PAYME_PRICE_HELPER
converter_amount_click = settings.CLICK_PRICE_HELPER


# from rest_framework_simplejwt import authentication


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

        if transaction_type == models.TRANSACTIONTYPECHOICES.PAYME:
            price = price * converter_amount

            generated_link = Paycom().create_initialization(
                price,
                transaction_id,
                return_url="/"
            )
        elif transaction_type == models.TRANSACTIONTYPECHOICES.CLICK:
            price = price * converter_amount_click

            generated_link = ClickUz.generate_url(
                order_id=transaction_id,
                amount=price,
                return_url='http://127.0.0.1:8000/dashboard/'
            )
        elif transaction_type == models.TRANSACTIONTYPECHOICES.VISA:
            pass

        return Response(
            status=status.HTTP_200_OK,
            data={"generated_link": generated_link}
        )


initialize_payment_api_view = InitializePaymentAPIView.as_view()


class AcceptPaymeRequestsView(MerchantAPIView):
    VALIDATE_CLASS = helper.CheckPayMeTransaction


accept_payme_request_view = AcceptPaymeRequestsView.as_view()


class AcceptClickRequestsView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = helper.CheckClickTransaction


accept_click_request_view = AcceptClickRequestsView.as_view()

