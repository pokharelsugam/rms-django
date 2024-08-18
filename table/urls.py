from django.urls import path
from . import views

urlpatterns = [

    path('', views.table_management, name='table_management'),
    # Table URLs
    path('num/', views.table, name='table'),
    path('num/<int:pk>/', views.table_detail, name='table_detail'),
    path('num/add/', views.table_add, name='table_add'),
    path('num/edit/<int:pk>/', views.table_edit, name='table_edit'),
    path('num/delete/<int:pk>/', views.table_delete, name='table_delete'),

    # Reservation URLs
    path('reservation/', views.reservation, name='reservation'),
    path('reservation/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservation/add/', views.reservation_add, name='reservation_add'),
    path('reservation/edit/<int:pk>/', views.reservation_edit, name='reservation_edit'),
    path('reservation/delete<int:pk>/', views.reservation_delete, name='reservation_delete'),

    # Seating URLs
    path('seating/', views.seating, name='seating'),
    path('seating/<int:pk>/', views.seating_detail, name='seating_detail'),
    path('seating/add/', views.seating_add, name='seating_add'),
    path('seating/edit/<int:pk>/', views.seating_edit, name='seating_edit'),
    path('seating/delete<int:pk>/', views.seating_delete, name='seating_delete'),
]
