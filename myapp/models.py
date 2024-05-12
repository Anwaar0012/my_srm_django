from django.db import models


# ======manager model==========
class Manager(models.Model):
    managersname = models.CharField(max_length=100)
    managersphonenumber = models.CharField(max_length=20)
    def __str__(self):
        return self.managersname
    
# Create your models here.
class ShopManager(models.Manager):
    def search(self, search_query=None):
        if search_query:
            return self.get_queryset().filter(
                models.Q(name__icontains=search_query) |
                models.Q(address__icontains=search_query) |
                models.Q(owner_number__icontains=search_query) |
                models.Q(owner_cnic__icontains=search_query)
            )
        else:
            return self.get_queryset()
        
class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    owner_number = models.CharField(max_length=20,null=True,blank=True)
    owner_cnic = models.CharField(max_length=15,null=True,blank=True)

    objects = ShopManager()

    def __str__(self):
        return self.name
    
# ======days model==========
class DaysEntry(models.Model):
    day_name = models.CharField(max_length=100)
    day_notes = models.TextField()

    def __str__(self):
        return self.day_name
    
# ======SalesPerson model==========
class SalesPerson(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
# ======Route model==========
class Route(models.Model):
    route_name = models.CharField(max_length=100)
    route_notes = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.route_name
    
class Routing(models.Model):
    day = models.ForeignKey(DaysEntry, on_delete=models.CASCADE)
    sales_person = models.ForeignKey(SalesPerson, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    routing= models.CharField(max_length=255, unique=True, editable=False,default="")
    routing_note= models.CharField(max_length=255, null=True,blank=True)

    def __str__(self):
        return self.routing

    def save(self, *args, **kwargs):
        # Concatenate values of related fields into routing
        self.routing = f"{self.sales_person.name} -> {self.day.day_name} -> {self.route.route_name} -> {self.shop.name} ({self.shop.address})"
        super().save(*args, **kwargs)

    
class Product(models.Model):
    crtn_pcs = models.CharField(max_length=80, null=True,blank=True)
    product_code = models.CharField(max_length=255,null=True,blank=True)
    product_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,blank=True,null=True)
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0,blank=True,null=True)

    def __str__(self):
        return f"{self.product_code} - {self.product_name}"
    
class Claim(models.Model):
    date = models.DateField()
    details = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')

    def __str__(self):
        return f"Claim #{self.id}"
    

