from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_management, name='inventory_management'),
    path('ingredient/', views.ingredient, name='ingredient'),
    path('ingredient/<int:pk>/', views.ingredient_detail, name='ingredient_detail'),
    path('ingredient/new/', views.ingredient_add, name='ingredient_add'),
    path('ingredient/edit/<int:pk>/', views.ingredient_edit, name='ingredient_edit'),
    path('ingredient/delete/<int:pk>/', views.ingredient_delete, name='ingredient_delete'),
    path('ingredientusage/', views.ingredientusage, name='ingredientusage'),
    path('ingredientusage/<int:pk>/', views.ingredientusage_detail, name='ingredientusage_detail'),
    path('ingredientusage/add/', views.ingredientusage_add, name='ingredientusage_add'),
    path('ingredientusage/edit/<int:pk>/', views.ingredientusage_edit, name='ingredientusage_edit'),
    path('ingredientusage/delete/<int:pk>/', views.ingredientusage_delete, name='ingredientusage_delete')
]
