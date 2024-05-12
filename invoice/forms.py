from datetime import datetime
from django import forms
from django.forms import formset_factory
from .models import Invoice, Recovery
from myapp.models import Product, Routing, SalesPerson, Shop,Manager
from django.utils import timezone

class InvoiceForm(forms.Form):
    SALE_TYPES = [
        ('------', '------'),
        ('Whole', 'Whole'),
        ('Retail', 'Retail'),
    ]

    customer = forms.ModelChoiceField(
        queryset=Shop.objects.all(),
        label='Customer',
        to_field_name='name',
        widget=forms.Select(attrs={
            'id': 'id_customer',  # Add the id attribute here
            'class': 'form-control',
        })
    )
    sale_types = forms.ChoiceField(
        choices=SALE_TYPES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    customer_email = forms.CharField(
        label='Contact',
        required=False,  # Set required attribute to False
        widget=forms.TextInput(attrs={
            'id': 'contact',
            'class': 'form-control',
            # 'placeholder': 'enter Customer No',
            'rows':1
        })
    )
    billing_address = forms.CharField(
        label='Billing Address',
        required=False,  # Set required attribute to False
        widget=forms.TextInput(attrs={
            'id': 'billing_address',
            'class': 'form-control',
            # 'placeholder': 'enter Customer No',
            'rows':1
        })
    )
    salesperson = forms.ModelChoiceField(
        queryset=SalesPerson.objects.all(),
        label='Salesperson',
        to_field_name='name',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    manager = forms.ModelChoiceField(
        queryset=Manager.objects.all(),
        label='Manager',
        to_field_name='managersname',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    routing = forms.ModelChoiceField(
        queryset=Routing.objects.all(),
        label='Routing / Route Mapping',
        to_field_name='routing',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    # due_date = forms.DateField(input_formats=['%Y-%m-%d', ''], required=False)
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False)

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        if due_date == '':
            cleaned_data['due_date'] = datetime.now().date()
        return cleaned_data

    def clean_manager(self):
        manager_name = self.cleaned_data.get('manager')
        if not manager_name:
            raise forms.ValidationError("Manager name is required.")

        try:
            manager = Manager.objects.get(managersname=manager_name)
        except Manager.DoesNotExist:
            raise forms.ValidationError("Manager with this name does not exist.")

        return manager


    def clean_customer(self):
        customer_name = self.cleaned_data['customer']
        shop = Shop.objects.get(name=customer_name)
        return shop
    
    def clean_salesperson(self):
        salesperson_name = self.cleaned_data.get('salesperson')
        if not salesperson_name:
            raise forms.ValidationError("Salesperson name is required.")

        try:
            salesperson = SalesPerson.objects.get(name=salesperson_name)
        except SalesPerson.DoesNotExist:
            raise forms.ValidationError("Salesperson not found.")

        return salesperson
    
    def clean_routing(self):
        routing_name = self.cleaned_data.get('routing')
        if not routing_name:
            raise forms.ValidationError("Salesperson name is required.")

        try:
            routing = Routing.objects.get(routing=routing_name)
        except SalesPerson.DoesNotExist:
            raise forms.ValidationError("Salesperson not found.")

        return routing
       
class LineItemForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label='Service/Product',
        to_field_name='product_name',        
        widget=forms.Select(attrs={
            # 'id': 'id_product_name',  # Add the id attribute here
            'class': 'form-control product-select',
        })
    )

    quantity = forms.DecimalField(
        label='Qty',
        required=True,  # Set required attribute to False
        # initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity',
            'step': '0.01',  # Adjust the step attribute for decimal input
            'min': '0'  # Set minimum value if applicable
        }) 
        
    )
    rate = forms.DecimalField(
        label='Rate ',
        required=True,  # Set required attribute to False
        widget=forms.NumberInput(attrs={
            # 'id': 'rate',
            'placeholder': 'rate',
            'class': 'form-control input rate myrate',
            'step': '0.01',  # Adjust the step attribute for decimal input
            'min': '0'  # Set minimum value if applicable
        })
        
    )
    # amount = forms.DecimalField(
    #     disabled = True,
    #     label='Amount $',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input',
    #     })
    # )
    def clean_customer(self):
        service_name = self.cleaned_data['service']
        product = Product.objects.get(product_name=service_name)
        return product
    
LineItemFormset = formset_factory(LineItemForm, extra=1)

class RecoveryForm(forms.ModelForm):
    class Meta:
        model = Recovery
        fields = ['invoice', 'customer', 'total_amount', 'date', 'amount_received', 'received_date','approved_by_manager']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'received_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
# class RecoveryForm(forms.ModelForm):
#     class Meta:
#         model = Recovery
#         fields = ['customer_name', 'total_amount', 'date', 'balance', 'new_paid_amount', 'current_balance']
#         widgets = {
#             'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
#         }