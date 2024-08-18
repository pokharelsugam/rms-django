from django.urls import path
from .views import menu_management,menuitem, menuitem_detail, menuitem_add, menuitem_edit, menuitem_delete, category,category_detail, category_add, category_edit, category_delete,customization, customization_detail, customization_add,customization_edit,customization_delete, get_customizations

urlpatterns = [
    path('', menu_management, name='menu_management'),
    path('item/', menuitem, name='menuitem'),
    path('item/<int:pk>/', menuitem_detail, name='menuitem_detail'),
    path('item/add/', menuitem_add, name='menuitem_add'),
    path('item/edit/<int:pk>/', menuitem_edit, name='menuitem_edit'),
    path('item/delete/<int:pk>/', menuitem_delete, name='menuitem_delete'),
    path('category/',category, name='category'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('category/add/', category_add, name='category_add'),
    path('category/edit/<int:pk>/', category_edit, name='category_edit'),
    path('category/delete/<int:pk>/',category_delete, name='category_delete'),
    path('customization/', customization, name='customization'),
    path('customization/<int:pk>/', customization_detail, name='customization_detail'),
    path('customization/add/', customization_add, name='customization_add'),
    path('customization/edit/<int:pk>/', customization_edit, name='customization_edit'),
    path('customization/delete/<int:pk>/', customization_delete, name='customization_delete'),
    path('get_customizations/',get_customizations, name='get_customizations'),
]