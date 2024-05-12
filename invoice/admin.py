from django.contrib import admin

from .models import Invoice, LineItem,Recovery,Transaction,CustomerAccount

admin.site.register(Invoice)
admin.site.register(LineItem)
admin.site.register(Recovery)
admin.site.register(Transaction)
# admin.site.register(CustomerAccount)
# Register your models here.
