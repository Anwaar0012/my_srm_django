
from django import forms

from .models import Claim, Product, Shop,Manager,DaysEntry,SalesPerson,Route,Route,Routing

class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['managersname', 'managersphonenumber']

class Days_Form(forms.ModelForm):
    class Meta:
        model = DaysEntry
        fields = ['day_name', 'day_notes']

class SalesPersonForm(forms.ModelForm):
    class Meta:
        model = SalesPerson
        fields = ['name', 'number']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['route_name', 'route_notes']

class RoutingForm(forms.ModelForm):
    class Meta:
        model = Routing
        fields = ['day', 'sales_person', 'route', 'shop']
        
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'address', 'owner_number', 'owner_cnic']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['crtn_pcs','product_code', 'product_name','quantity','price']

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['date','details', 'amount','status']