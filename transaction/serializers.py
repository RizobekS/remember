from abc import ABC

from rest_framework import serializers
from transaction.models import TRANSACTIONTYPECHOICES, Transaction


class InitializePaymentSerializer(serializers.Serializer, ABC):
    transaction_type = serializers.ChoiceField(
        choices=TRANSACTIONTYPECHOICES.choices,
    )
    price = serializers.DecimalField(max_digits=20, decimal_places=3)
