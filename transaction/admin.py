from django.contrib import admin
from transaction.models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['owner', 'service', 'total_price']


admin.site.register(Transaction, TransactionAdmin)
