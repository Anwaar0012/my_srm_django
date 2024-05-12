from django.urls import path
from . import views
# from .models import views.TransactionListView



urlpatterns = [
    # path('', views.index, name='index'),

    path('managers/', views.managers, name='managers'),
    path('add-manager/', views.add_manager, name='add_manager'),
    path('edit-manager/<int:manager_id>/', views.edit_manager, name='edit_manager'),
    path('delete-manager/<int:manager_id>/', views.delete_manager, name='delete_manager'),
    
    path('shops/', views.shop_list, name='shop_list'),
    path('add_shop/', views.add_shop, name='add_shop'),
    path('edit_shop/<int:pk>/', views.edit_shop, name='edit_shop'),
    path('delete_shop/<int:pk>/', views.delete_shop, name='delete_shop'),

    path('products/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),

    path('days/', views.days_list, name='days'),
    path('add_days/', views.add_day, name='add_days'),
    path('edit_day/<int:pk>/', views.edit_day, name='edit_day'),
    path('delete_day/<int:pk>/', views.delete_day, name='delete_day'),

    path('sales_persons/', views.sales_person_list, name='sales_person_list'),
    path('add_sales_person/', views.add_sales_person, name='add_sales_person'),
    path('edit_sales_person/<int:pk>/', views.edit_sales_person, name='edit_sales_person'),
    path('delete_sales_person/<int:pk>/', views.delete_sales_person, name='delete_sales_person'),

    path('routes/', views.route_list, name='route_list'),
    path('add_route/', views.add_route, name='add_route'),
    path('edit_route/<int:pk>/', views.edit_route, name='edit_route'),
    path('delete_route/<int:pk>/', views.delete_route, name='delete_route'),

    path('routings/', views.routing_list, name='routing_list'),
    path('add_routing/', views.routing_create, name='add_routing'),
    path('edit_routing/<int:pk>/', views.edit_routing, name='edit_routing'),
    path('delete_routing/<int:pk>/', views.routing_delete, name='delete_routing'),

    path('claims/', views.claims_list, name='claim_list'),
    path('add_claim/', views.claim_create, name='add_claim'),
    path('edit_claim/<int:pk>/', views.edit_claim, name='edit_claim'),
    path('delete_claim/<int:pk>/', views.claim_delete, name='delete_claim'),

    path('transactions/', views.transaction_list, name='transaction_list'),
    # path('transactions/', views.create_transaction, name='transaction_list'),
    # path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('delete_transactions/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),

]