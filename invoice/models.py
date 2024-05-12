from decimal import Decimal
from django.db import models
import datetime
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.
class InvoiceManager(models.Manager):
    def search(self, search_query=None):
        if search_query:
            return self.get_queryset().filter(
                models.Q(customer__icontains=search_query) |
                models.Q(salesperson__icontains=search_query) |
                models.Q(manager__icontains=search_query) |
                models.Q(date__icontains=search_query)
            )
        else:
            return self.get_queryset()
    
class Invoice(models.Model):
    customer = models.CharField(max_length=100)
    customer_email = models.TextField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2,default=0)
    salesperson = models.CharField(max_length=100, blank=True, null=True)
    manager = models.CharField(max_length=100, blank=True, null=True)
    routing = models.CharField(max_length=255, blank=True, null=True)
    sale_types = models.CharField(max_length=255, blank=True, null=True)

    objects = InvoiceManager()

    def __str__(self):
        return str(self.customer)
    

    
    

    # def save(self, *args, **kwargs):
        # if not self.id:             
        #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
        # return super(Invoice, self).save(*args, **kwargs)

class LineItem(models.Model):
    customer = models.ForeignKey(Invoice,on_delete=models.CASCADE, blank=True, null=True)
    service = models.TextField()
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.customer)
    

# Create your models here.
# class RecoveryManager(models.Manager):
#     def search(self, search_query=None):
#         if search_query:
#             return self.get_queryset().filter(
#                 models.Q(name__icontains=search_query) |
#                 models.Q(address__icontains=search_query) |
#                 models.Q(owner_number__icontains=search_query) |
#                 models.Q(owner_cnic__icontains=search_query)
#             )
#         else:
#             return self.get_queryset()
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

class CustomerAccount(models.Model):
    customer = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.customer
    
    @staticmethod
    @receiver(post_save, sender=Invoice)
    def update_customer_account(sender, instance, **kwargs):
        # Get or create CustomerAccount instance for the customer
        customer_account, created = CustomerAccount.objects.get_or_create(customer=instance.customer)
        
        # Update total_amount based on the sum of total_amount of all invoices for this customer
        customer_account.total_amount = Invoice.objects.filter(customer=instance.customer).aggregate(total=Sum('total_amount'))['total'] or 0
        customer_account.save()

from django.core.validators import MinValueValidator 

class Recovery(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name='recoveries')
    customer = models.CharField(max_length=100, null=True, blank=True,)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField(default=None)
    amount_received = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    received_date = models.DateField(default=None)
    balance=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    previous_balance=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    approved_by_manager = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # Set default dates if not provided
        self._set_default_dates()

        # Ensure total_amount and paid_amount are Decimal objects
        # self._convert_decimal_fields(['total_amount', 'amount_received'])

        # # Calculate balance if total_amount and amount_received are provided
        # if self.total_amount is not None and self.amount_received is not None:
        #     self.balance = self.total_amount - self.amount_received

        super().save(*args, **kwargs)

    def _set_default_dates(self):
        if not self.date:
            self.date = self._get_default_date()
        if not self.received_date:
            self.received_date = timezone.now().date()

    def _get_default_date(self):
        if self.invoice and self.invoice.date:
            return self.invoice.date
        return timezone.now().date()

    # def _convert_decimal_fields(self, field_names):
    #     for field_name in field_names:
    #         field_value = getattr(self, field_name)
    #         if isinstance(field_value, str):
    #             setattr(self, field_name, Decimal(field_value))

    def __str__(self):
        return f"Recovery for {self.customer} on {self.date} & updated on {self.received_date}"
    

    
class Transaction(models.Model):
    recovery = models.ForeignKey('Recovery', on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    customer = models.CharField(max_length=100, null=True, blank=True,)
    manager = models.CharField(max_length=100, blank=True, null=True)
    salesperson = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    routing = models.CharField(max_length=255, blank=True, null=True)
    sale_types = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)    
    amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Ensure total_amount and amount are Decimal objects
        self._convert_decimal_fields(['total_amount', 'amount'])

        # Calculate balance if total_amount and amount are provided
        if self.total_amount is not None and self.amount is not None:
            self.balance = self.total_amount - self.amount

        super().save(*args, **kwargs)
    
    def _convert_decimal_fields(self, field_names):
        for field_name in field_names:
            field_value = getattr(self, field_name)
            if isinstance(field_value, str):
                setattr(self, field_name, Decimal(field_value))
    
    def __str__(self):
        return self.customer

    

# @receiver(post_delete, sender=Transaction)
# def delete_related_invoice_or_recovery(sender, instance, **kwargs):
#     if instance.invoice:
#         instance.invoice.delete()
#     elif instance.recovery:
#         instance.recovery.delete()
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db.models import Sum

# class CustomerAccount(models.Model):
#     customer = models.CharField(max_length=100, unique=True)
#     total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

#     def __str__(self):
#         return self.customer
    
#     @staticmethod
#     @receiver(post_save, sender=Invoice)
#     def update_customer_account(sender, instance, **kwargs):
#         # Get or create CustomerAccount instance for the customer
#         customer_account, created = CustomerAccount.objects.get_or_create(customer=instance.customer)
        
#         # Update total_amount based on the sum of total_amount of all invoices for this customer
#         customer_account.total_amount = Invoice.objects.filter(customer=instance.customer).aggregate(total=Sum('total_amount'))['total'] or 0
#         customer_account.save()
