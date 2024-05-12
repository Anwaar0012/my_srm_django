import datetime
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from invoice.models import Invoice
from .models import  Claim, Manager, Product, DaysEntry,SalesPerson,Route,Shop,Routing
from .forms import ClaimForm, ManagerForm,Days_Form,SalesPersonForm,RouteForm,ShopForm,RoutingForm,ProductForm
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q

# HOME VIEW 
def index(request):
    total_sales = Transaction.objects.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    total_payments = Transaction.objects.aggregate(total_payments=Sum('amount'))['total_payments'] or 0
    total_balance = Transaction.objects.aggregate(total_balance=Sum('balance'))['total_balance'] or 0

    total_sales = total_sales if total_sales is not None else 0
    total_payments = total_payments if total_payments is not None else 0
    total_balance = total_balance if total_balance is not None else 0
    context = {
        'total_sales': total_sales,
        'total_payments': total_payments,
        'total_balance': total_balance
    }
    return render(request, 'index.html',context)

def managers(request):
    managers = Manager.objects.all()
    return render(request, 'myapp/managers/managers.html', {'managers': managers})

@login_required
def add_manager(request):
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,  ("Change made successfully.")) 
            return redirect('managers')
    
    else:
        form = ManagerForm()
    return render(request, 'myapp/managers/add_manager.html', {'form': form})

def edit_manager(request, manager_id):
    manager = get_object_or_404(Manager, id=manager_id)
    if request.method == 'POST':
        form = ManagerForm(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('managers')
    else:
        form = ManagerForm(instance=manager)
    return render(request, 'myapp/managers/edit_manager.html', {'form': form, 'manager': manager})

def delete_manager(request, manager_id):
    manager = get_object_or_404(Manager, id=manager_id)
    if request.method == 'POST':
        manager.delete()
        return redirect('managers')
    return render(request, 'myapp/managers/delete_manager_confirm.html', {'manager': manager})


def days_list(request):
    days_fetched = DaysEntry.objects.all()
    # print(days_fetched)
    return render(request, 'myapp/days/days_list.html', {'days_fetched': days_fetched})

def add_day(request):
    if request.method == 'POST':
        form = Days_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('days')
    else:
        form = Days_Form()
    return render(request, 'myapp/days/add_day.html', {'form': form})

def edit_day(request, pk):
    day = get_object_or_404(DaysEntry, pk=pk)
    if request.method == 'POST':
        form = Days_Form(request.POST, instance=day)
        if form.is_valid():
            form.save()
            return redirect('days')
    else:
        form = Days_Form(instance=day)
    return render(request, 'myapp/days/edit_day.html', {'form': form})

def delete_day(request, pk):
    day = get_object_or_404(DaysEntry, pk=pk)
    if request.method == 'POST':
        day.delete()
        return redirect('days')
    return render(request, 'myapp/days/delete_day.html', {'day': day})

#=== sales_person_list views function  
def sales_person_list(request):
    sales_persons = SalesPerson.objects.all()
    return render(request, 'myapp/sales/sales_person_list.html', {'sales_persons': sales_persons})

#=== add_sales_person views function
def add_sales_person(request):
    if request.method == 'POST':
        form = SalesPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_person_list')
    else:
        form = SalesPersonForm()
    return render(request, 'myapp/sales/add_sales_person.html', {'form': form})

#=== edit_sales_person views function 
def edit_sales_person(request, pk):
    sales_person = get_object_or_404(SalesPerson, pk=pk)
    if request.method == 'POST':
        form = SalesPersonForm(request.POST, instance=sales_person)
        if form.is_valid():
            form.save()
            return redirect('sales_person_list')
    else:
        form = SalesPersonForm(instance=sales_person)
    return render(request, 'myapp/sales/edit_sales_person.html', {'form': form})

#=== delete_sales_person views function 
def delete_sales_person(request, pk):
    sales_person = get_object_or_404(SalesPerson, pk=pk)
    if request.method == 'POST':
        sales_person.delete()
        return redirect('sales_person_list')
    return render(request, 'myapp/sales/delete_sales_person.html', {'sales_person': sales_person})

#=== route_list views function 
def route_list(request):
    routes = Route.objects.all().order_by('-id')
    return render(request, 'myapp/routes/route_list.html', {'routes': routes})

#=== add_route views function
def add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        form = RouteForm()
    return render(request, 'myapp/routes/add_route.html', {'form': form})

#=== edit_route views function
def edit_route(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        form = RouteForm(instance=route)
    return render(request, 'myapp/routes/edit_route.html', {'form': form})

#=== delete_route views function
def delete_route(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        route.delete()
        return redirect('route_list')
    return render(request, 'myapp/routes/delete_route.html', {'route': route})

#=== shop_list views function
def shop_list(request):
    # search_query = request.GET.get('q', '')
    # if search_query:  # If a search query is provided
    #     shops = Shop.objects.search(search_query).order_by('-id')
    # else:
    shops = Shop.objects.all().order_by('-id')
    # shops = Shop.objects.order_by('-id')
    return render(request, 'myapp/shops/shop_list.html', {'shops': shops})

#=== shop_list views function
def add_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm()
    return render(request, 'myapp/shops/add_shop.html', {'form': form})

#=== edit_shop views function
def edit_shop(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm(instance=shop)
    return render(request, 'myapp/shops/edit_shop.html', {'form': form})

#=== delete_shop views function
def delete_shop(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        shop.delete()
        return redirect('shop_list')
    return render(request, 'myapp/shops/delete_shop.html', {'shop': shop})

#=== product_list views function
def product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'myapp/product/product_list.html', {'products': products})

#=== add_product views function
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'myapp/product/add_product.html', {'form': form, 'action': 'Add'})

#=== edit_product views function
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myapp/product/edit_product.html', {'form': form, 'action': 'Edit'})

#=== delete_product views function
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'myapp/product/delete_product.html', {'product': product})

#=== routing_list views function
def routing_list(request):
    routings = Routing.objects.all().order_by('-id')
    return render(request, 'myapp/routing/routing_list.html', {'routings': routings})

#=== routing_create views function
def routing_create(request):
    if request.method == 'POST':
        form = RoutingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('routing_list')
    else:
        form = RoutingForm()
    return render(request, 'myapp/routing/add_routing.html', {'form': form})

#=== edit_routing views function
def edit_routing(request, pk):
    routing = get_object_or_404(Routing, pk=pk)
    if request.method == 'POST':
        form = RoutingForm(request.POST, instance=routing)
        if form.is_valid():
            form.save()
            return redirect('routing_list')
    else:
        form = RoutingForm(instance=routing)
    return render(request, 'myapp/routing/edit_routing.html', {'form': form})

#=== routing_delete views function
def routing_delete(request, pk):
    routing = get_object_or_404(Routing, pk=pk)
    if request.method == 'POST':
        routing.delete()
        return redirect('routing_list')
    return render(request, 'myapp/routing/delete_routing.html', {'routing': routing})


#=== routing_list views function
def claims_list(request):
    claims = Claim.objects.all().order_by('-id')
    return render(request, 'myapp/claim/claims_list.html', {'claims': claims})

#=== routing_create views function
def claim_create(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('claim_list')
    else:
        form = ClaimForm()
    return render(request, 'myapp/claim/add_claim.html', {'form': form})

def edit_claim(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    if request.method == 'POST':
        form = ClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            return redirect('claim_list')
    else:
        form = ClaimForm(instance=claim)
    return render(request, 'myapp/claim/edit_claim.html', {'form': form})

#=== routing_delete views function
def claim_delete(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    if request.method == 'POST':
        claim.delete()
        return redirect('claim_list')
    return render(request, 'myapp/claim/delete_claim.html', {'claim': claim})

from invoice.models import Transaction,Recovery
def transaction_list(request):
    search_query = request.GET.get('q', '')  # Get the search query from the request GET parameters
    start_date_str = request.GET.get('start_date', '')  # Get the start date from the request GET parameters
    end_date_str = request.GET.get('end_date', '')  # Get the end date from the request GET parameters

    # Convert date strings to datetime objects
    start_date = None
    end_date = None
    if start_date_str:
        start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
    if end_date_str:
        end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1))

    if search_query:  # If a search query is provided
        query = Q(customer__icontains=search_query) 
        transactions = Transaction.objects.filter(query).order_by('-id')
    elif start_date and end_date:  # If start date and end date are provided
        transactions = Transaction.objects.filter(due_date__range=(start_date, end_date)).order_by('-id')
    else:
        transactions = Transaction.objects.all().order_by('-id')

    return render(request, 'myapp/transaction/transaction_list.html', {'transactions': transactions})


#=== add_transaction views function
# def add_transaction(request):
#     if request.method == 'POST':
#         form = (request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionForm()
#     return render(request, 'myapp/transaction/add_transaction.html', {'form': form})

#=== edit_transaction views function
# def edit_transaction(request, transaction_id):
#     transaction = Transaction.objects.get(pk=transaction_id)
#     if request.method == 'POST':
#         form = TransactionForm(request.POST, instance=transaction)
#         if form.is_valid():
#             form.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionForm(instance=transaction)
#     return render(request, 'myapp/transaction/edit_transaction.html', {'form': form})

#=== delete_transaction views function
def delete_transaction(request, pk):
    transaction = Invoice.objects.get(pk=pk)
    print(transaction.id)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'myapp/transaction/delete_transaction.html', {'transaction': transaction})

