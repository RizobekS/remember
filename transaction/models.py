from django.db import models
from rememberApp.models import *


class TRANSACTIONTYPECHOICES(models.TextChoices):
    PAYME = "payme"
    CLICK = "click"
    VISA = "visa"


class TRANSACTIONSTATUS(models.TextChoices):
    NEW = "new"
    VERIFIED = "verified"
    PAID = "paid"
    CANCELED = "canceled"


class Transaction(models.Model):
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)
    price = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True)

    total_price = models.DecimalField(max_digits=20, decimal_places=3)
    is_verified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transactions', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTIONTYPECHOICES.choices)
    status = models.CharField(max_length=10, choices=TRANSACTIONSTATUS.choices, default=TRANSACTIONSTATUS.NEW)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def verify(self):
        self.status = TRANSACTIONSTATUS.VERIFIED
        self.is_verified = True
        self.save()

    def make_payment(self):
        self.status = TRANSACTIONSTATUS.PAID
        self.is_paid = True
        self.save()

    def cancel(self):
        self.status = TRANSACTIONSTATUS.CANCELED
        self.is_canceled = True
        self.is_paid = False
        self.save()

    def __str__(self):
        return f"{str(self.owner)}   {str(self.total_price)}"
