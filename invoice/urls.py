from django.contrib import admin
from django.urls import path
from .views import InvoiceListView, createInvoice, view_PDF,get_details_customer,get_product_rate,generate_invoice_excel_report,generate_shop_excel_report,generate_recoveries_excel_report,delete_invoice,editInvoice,recovery_list,create_recovery,invoice_list_recovery,manager_approval,delete_recovery

app_name = 'invoice'
urlpatterns = [
    path('', InvoiceListView.as_view(), name="invoice-list"),
    path('invoice/create/', createInvoice, name="invoice-create"),
    path('invoice-detail/<id>', view_PDF, name='invoice-detail'),
    path('invoice-delete/<id>', delete_invoice, name='invoice-delete'),
    path('invoice-edit/<id>', editInvoice, name='invoice-edit'),
    # path('invoice-download/<id>', generate_PDF, name='invoice-download'),
    # path('create-recovery/<id>', create_recovery, name='create-recovery'),
    path('create-recovery/<customer_name>/', create_recovery, name='create-recovery'),
    path('recovery-list/',recovery_list, name='recovery-list'),
    path('manager-approval/<int:recovery_id>/<int:invoice_id>/', manager_approval, name='manager_approval'),
    path('invoice_list_recovery/',invoice_list_recovery, name='invoice_list_recovery'),
    # path('edit_recovery/<int:pk>/', edit_recovery, name='edit_recovery'),
    path('delete_recovery/<int:pk>/', delete_recovery, name='delete_recovery'),
    path('get-customer-details/<str:shop_name>/', get_details_customer, name='get_customer_details'),
    path('get-product-rate/<str:product_name>/', get_product_rate, name='get_product_rate'),
    path('gen-report-invoice/', generate_invoice_excel_report, name='generate_invoice_report'),
    path('gen-report-shops/', generate_shop_excel_report, name='generate_shops_report'),
    path('gen-report-recovery/', generate_recoveries_excel_report, name='generate_recovery_report'),


]
