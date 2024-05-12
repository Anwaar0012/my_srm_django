from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Manager,DaysEntry,SalesPerson,Route,Shop,Routing,Product,Claim
class ShopAdmin(admin.ModelAdmin):
    admin.site.site_header = 'Sales Persons Relationship Management System'
    admin.site.register(Manager)
    admin.site.register(DaysEntry)
    admin.site.register(SalesPerson)
    admin.site.register(Route)
    admin.site.register(Routing)
    admin.site.register(Shop)
    admin.site.register(Product)
    admin.site.register(Claim)