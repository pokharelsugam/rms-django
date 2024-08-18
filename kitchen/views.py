from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from order.models import Order, SpecialOrder

def kitchendisplay(request):
    orders = Order.objects.all()
    special_orders = SpecialOrder.objects.all()
    return render(request, 'kitchendisplay.html', {'orders': orders, 'special_orders': special_orders})

@login_required
def kitchendisplay_detail(request, order_type, pk):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied 
    if order_type == 'order':
        kitchen_order = get_object_or_404(Order, id=pk)
    else:
        kitchen_order = get_object_or_404(SpecialOrder, id=pk)
    
    return render(request, 'kitchendisplay-detail.html', {'kitchen_order': kitchen_order, 'order_type': order_type})

@login_required
def kitchendisplay_update_order_status(request, order_type, pk):
    if not (request.user.is_admin or request.user.is_chef):
        raise PermissionDenied
    if order_type == 'order':
        kitchen_order = get_object_or_404(Order, id=pk)
    else:
        kitchen_order = get_object_or_404(SpecialOrder, id=pk)

    if request.method == 'POST':
        new_order_status = request.POST.get('order_status')
        order_status_choices = dict(Order.ORDER_STATUS_CHOICES) if order_type == 'order' else dict(SpecialOrder.ORDER_STATUS_CHOICES)
        if new_order_status in order_status_choices.keys():
            kitchen_order.order_status = new_order_status
            kitchen_order.updated_by = request.user
            kitchen_order.save()
    return redirect('kitchendisplay_detail', order_type=order_type, pk=pk)
