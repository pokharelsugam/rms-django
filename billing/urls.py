from django.urls import path
from .views import billing_management,bill_create, bill_detail, bill, update_bill_status

urlpatterns = [
    path('', billing_management, name='billing_management'),
    path('bill/create/', bill_create, name='bill_create'),
    path('bill/<int:bill_id>/', bill_detail, name='bill_detail'),
    path('bills/', bill, name='bill'),
    path('bill/paid/<int:bill_id>/',update_bill_status, {'status': 'PD'}, name='mark_bill_as_paid'),
    path('bill/refunded/<int:bill_id>/', update_bill_status, {'status': 'RF'}, name='mark_bill_as_refunded'),
]
