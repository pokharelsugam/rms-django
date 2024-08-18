from django.urls import path
from . import views

urlpatterns = [
    path('', views.kitchendisplay, name='kitchendisplay'),
    path('<str:order_type>/<int:pk>/', views.kitchendisplay_detail, name='kitchendisplay_detail'),
    path('update-order_status/<str:order_type>/<int:pk>/', views.kitchendisplay_update_order_status, name='kitchendisplay_update_order_status'),
]
