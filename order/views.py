from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem, SpecialOrder
from django.core.exceptions import PermissionDenied
from .forms import OrderForm, OrderItemForm, SpecialOrderForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def order_management(request):
    return render(request, 'order-management.html')

@login_required
def order(request):
    orders = Order.objects.all()
    return render(request, 'order.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_waiter or request.user.is_chef):
        raise PermissionDenied 
    order = get_object_or_404(Order, id=pk)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order-detail.html', {'order': order, 'order_items': order_items})

@login_required
def order_add(request):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied 
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            
            return redirect('order_detail', pk=order.id)
    else:
        form = OrderForm()
    return render(request, 'order-add-edit.html', {'form': form})

@login_required
def order_edit(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit= False)
            order.updated_by = request.user
            order.save()
            return redirect('order_detail', pk=order.id)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order-add-edit.html', {'form': form})

@login_required
def order_delete(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order')
    return render(request, 'order-delete-confirm.html', {'order': order})

# OrderItem views
@login_required
def orderitem(request):
    order_items = OrderItem.objects.all()
    return render(request, 'orderitem.html', {'order_items': order_items})

@login_required
def orderitem_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_waiter or request.user.is_chef):
        raise PermissionDenied
    order_item = get_object_or_404(OrderItem, id=pk)
    return render(request, 'orderitem-detail.html', {'order_item': order_item})

@login_required
def orderitem_add(request, order_pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    order = get_object_or_404(Order, id=order_pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            form.save_m2m()
            return redirect('order_detail', pk=order.id)
    else:
        form = OrderItemForm()
    return render(request, 'orderitem-add-edit.html', {'form': form, 'order': order})

@login_required
def orderitem_edit(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    order_item = get_object_or_404(OrderItem, id=pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=order_item.order.id)
    else:
        form = OrderItemForm(instance=order_item)
    return render(request, 'orderitem-add-edit.html', {'form': form, 'order': order_item.order})

@login_required
def orderitem_delete(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    order_item = get_object_or_404(OrderItem, id=pk)
    order_pk = order_item.order.id
    if request.method == 'POST':
        order_item.delete()
        return redirect('order_detail', pk=order_pk)
    return render(request, 'orderitem-delete-confirm.html', {'order_item': order_item})

# List all special orders
@login_required
def specialorder(request):
    special_orders = SpecialOrder.objects.all()
    return render(request, 'specialorder.html', {'special_orders': special_orders})

# View details of a specific special order
@login_required
def specialorder_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_waiter or request.user.is_chef):
        raise PermissionDenied
    special_order = get_object_or_404(SpecialOrder, id=pk)
    return render(request, 'specialorder-detail.html', {'special_order': special_order})

# Add a new special order
@login_required
def specialorder_add(request):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    if request.method == 'POST':
        form = SpecialOrderForm(request.POST)
        if form.is_valid():
            special_order = form.save(commit= False)
            special_order.created_by = request.user
            special_order.save()
            return redirect('specialorder_detail', pk=special_order.id)
    else:
        form = SpecialOrderForm()
    return render(request, 'specialorder-add-edit.html', {'form': form})

# Edit an existing special order
@login_required
def specialorder_edit(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    special_order = get_object_or_404(SpecialOrder, id=pk)
    if request.method == 'POST':
        form = SpecialOrderForm(request.POST, instance=special_order)
        if form.is_valid():
            special_order = form.save(commit= False)
            special_order.updated_by = request.user
            special_order.save()
            return redirect('specialorder_detail', pk=special_order.id)
    else:
        form = SpecialOrderForm(instance=special_order)
    return render(request, 'specialorder-add-edit.html', {'form': form})

# Delete a special order
@login_required
def specialorder_delete(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    special_order = get_object_or_404(SpecialOrder, id=pk)
    if request.method == 'POST':
        special_order.delete()
        return redirect('specialorder')
    return render(request, 'specialorder-delete-confirm.html', {'special_order': special_order})

