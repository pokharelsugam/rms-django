from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_management, name = 'order_management'),
    path('num', views.order, name='order'),
    path('num/<int:pk>/', views.order_detail, name='order_detail'),
    path('num/add/', views.order_add, name='order_add'),
    path('num/edit/<int:pk>/', views.order_edit, name='order_edit'),
    path('num/delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('orderitem', views.orderitem, name='orderitem'),
    path('orderitem/<int:pk>/', views.orderitem_detail, name='orderitem_detail'),
    path('num/item/add/<int:order_pk>/', views.orderitem_add, name='orderitem_add'),
    path('orderitem/edit/<int:pk>/', views.orderitem_edit, name='orderitem_edit'),
    path('orderitem/delete/<int:pk>/', views.orderitem_delete, name='orderitem_delete'),
    path('specialorder/', views.specialorder, name='specialorder'),
    path('specialorder/<int:pk>/', views.specialorder_detail, name='specialorder_detail'),
    path('specialorder/add/', views.specialorder_add, name='specialorder_add'),
    path('specialorder/edit/<int:pk>/', views.specialorder_edit, name='specialorder_edit'),
    path('specialorder/delete/<int:pk>/', views.specialorder_delete, name='specialorder_delete'),
]
