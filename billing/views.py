from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Bill, BillItem
from django.contrib import messages
from order.models import Order, SpecialOrder
from .forms import BillGenerationForm
from num2words import num2words


def billing_management(request):
    return render(request,'billing-management.html')

@login_required
def bill_create(request):
    if not (request.user.is_admin or request.user.is_cashier):
        raise PermissionDenied
    if request.method == 'POST':
        form = BillGenerationForm(request.POST)
        if form.is_valid():
            bill_type = form.cleaned_data['bill_type']
            order_number = form.cleaned_data['order_number']
            bill = None

            if bill_type == 'order':
                try:
                    order = Order.objects.get(order_number=order_number)
                    existing_bill = Bill.objects.filter(order=order).first()
                    if existing_bill:
                        messages.error(request, f'Bill already exists for Order {order_number}.')
                        return redirect('bill_create')

                    bill = Bill(
                        order=order,
                        customer_name=order.customer_name,
                        total_amount=0,  # Placeholder value
                        created_by=request.user
                    )
                    bill.save()  # Save to generate bill_number

                    # Create BillItems for the Order
                    for order_item in order.orders.all():  # Note: using order.orders.all() to fetch related OrderItems
                        BillItem.objects.create(
                            bill=bill,
                            item_type='order',
                            order_item=order_item,
                            quantity=order_item.quantity,
                            price=order_item.get_customized_order_price(),
                            subtotal=order_item.get_total_price()
                        )

                    # Update payment_status of the Order
                    order.payment_status = 'UP'
                    order.save()

                except Order.DoesNotExist:
                    messages.error(request, f'Order with number {order_number} does not exist.')
                    return redirect('bill_create')

            elif bill_type == 'special':
                try:
                    special_order = SpecialOrder.objects.get(order_number=order_number)
                    existing_bill = Bill.objects.filter(special_order=special_order).first()
                    if existing_bill:
                        messages.error(request, f'Bill already exists for Special Order {order_number}.')
                        return redirect('bill_create')

                    bill = Bill(
                        special_order=special_order,
                        customer_name=special_order.customer_name,
                        total_amount=0,  # Placeholder value
                        created_by=request.user
                    )
                    bill.save()  # Save to generate bill_number

                    # Create BillItems for the Special Order
                    BillItem.objects.create(
                        bill=bill,
                        item_type='special',
                        special_order_item=special_order,
                        quantity=special_order.quantity,
                        price=special_order.price,
                        subtotal=special_order.total_price
                    )

                    # Update payment_status of the Special Order
                    special_order.payment_status = 'UP'
                    special_order.save()

                except SpecialOrder.DoesNotExist:
                    messages.error(request, f'Special Order with number {order_number} does not exist.')
                    return redirect('bill_create')

            # Update the total amount of the bill
            bill.total_amount = sum(item.subtotal for item in bill.bill_items.all())
            bill.save()

            messages.success(request, f'Bill {bill.bill_number} generated successfully.')
            return redirect('bill_detail', bill_id=bill.id)  # Redirect to the bill detail page

    else:
        form = BillGenerationForm()

    return render(request, 'bill-create.html', {'form': form})

@login_required
def bill_detail(request, bill_id):
    if not (request.user.is_admin or request.user.is_cashier or request.user.is_manager):
        raise PermissionDenied
    bill = get_object_or_404(Bill, id=bill_id)
    total_amount_in_words = num2words(bill.total_amount)

    context = {
        'bill': bill,
        'total_amount_in_words': total_amount_in_words,
    }
    return render(request, 'bill-detail.html', context)

@login_required
def bill(request):
    bills = Bill.objects.all()
    return render(request, 'bill.html', {'bills': bills})


@login_required
def update_bill_status(request, bill_id, status):
    if not (request.user.is_admin or request.user.is_cashier):
        raise PermissionDenied
    bill = get_object_or_404(Bill, id=bill_id)
    
    if status not in ['PD', 'RF']:
        messages.error(request, 'Invalid status.')
        return redirect('bill_detail', bill_id=bill.id)

    # Update the payment status of the bill
    bill.payment_status = status
    bill.save()

    if bill.order:
        # Also update the payment status of the associated order
        bill.order.payment_status = status
        bill.order.save()

    if bill.special_order:
        # Also update the payment status of the associated special order
        bill.special_order.payment_status = status
        bill.special_order.save()

    messages.success(request, f'Bill {bill.bill_number} marked as {"paid" if status == "PD" else "refunded"} successfully.')
    return redirect('bill_detail', bill_id=bill.id)