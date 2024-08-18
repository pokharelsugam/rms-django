from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Category, MenuItem, Customization
from .forms import CategoryForm, MenuItemForm, CustomizationForm
from django.http import JsonResponse

# Create your views here.

def menu_management(request):
    return render(request, 'menu-management.html')

# Category views

@login_required
def category(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})


@login_required
def category_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    category_obj = get_object_or_404(Category, id=pk)
    return render(request, 'category-detail.html', {'category': category_obj})

@login_required
def category_add(request):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm()
    return render(request, 'category-add-edit.html', {'form': form})

@login_required
def category_edit(request, pk):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category-add-edit.html', {'form': form})

@login_required
def category_delete(request, pk):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category')
    return render(request, 'category-delete-confirm.html', {'category': category})

# MenuItem views

@login_required
def menuitem(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menuitem.html', {'menu_items': menu_items})

@login_required
def menuitem_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef or request.user.is_waiter):
        raise PermissionDenied
    menu_item = get_object_or_404(MenuItem, id=pk)
    return render(request, 'menuitem-detail.html', {'menu_item': menu_item})

@login_required
def menuitem_add(request):
    if not (request.user.is_admin or request.user.is_chef or request.user.is_waiter):
        raise PermissionDenied
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menuitem')
    else:
        form = MenuItemForm()
    return render(request, 'menuitem-add-edit.html', {'form': form})

@login_required
def menuitem_edit(request, pk):
    if not (request.user.is_admin or request.user.is_chef or request.user.is_waiter):
        raise PermissionDenied
    menu_item = get_object_or_404(MenuItem, id=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('menuitem')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'menuitem-add-edit.html', {'form': form})

@login_required
def menuitem_delete(request, pk):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied
    menu_item = get_object_or_404(MenuItem, id=pk)
    if request.method == 'POST':
        menu_item.delete()
        return redirect('menuitem')
    return render(request, 'menuitem-delete-confirm.html', {'menu_item': menu_item})

@login_required
def customization(request):
    customizations = Customization.objects.all()
    return render(request, 'customization.html', {'customizations': customizations})

@login_required
def customization_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef or request.user.is_waiter):
        raise PermissionDenied
    customization = get_object_or_404(Customization, id=pk)
    return render(request, 'customization-detail.html', {'customization': customization})

@login_required
def customization_add(request):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied
    if request.method == 'POST':
        form = CustomizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customization')
    else:
        form = CustomizationForm()
    return render(request, 'customization-add-edit.html', {'form': form})

@login_required
def customization_edit(request, pk):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied
    customization = get_object_or_404(Customization, pk=pk)
    if request.method == 'POST':
        form = CustomizationForm(request.POST, instance=customization)
        if form.is_valid():
            form.save()
            return redirect('customization')
    else:
        form = CustomizationForm(instance=customization)
    return render(request, 'customization-add-edit.html', {'form': form})

@login_required
def customization_delete(request, pk):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied
    customization = get_object_or_404(Customization, pk=pk)
    if request.method == 'POST':
        customization.delete()
        return redirect('customization')
    return render(request, 'customization-delete-confirm.html', {'customization': customization})

@login_required
def get_customizations(request):
    category_id = request.GET.get('category_id')
    customizations = Customization.objects.filter(category_id=category_id)
    options = ''.join([f'<option value="{customization.id}">{customization.name} ({customization.price})</option>' for customization in customizations])
    return JsonResponse(options, safe=False)