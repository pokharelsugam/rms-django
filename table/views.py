from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Table, Reservation, Seating
from .forms import TableForm, ReservationForm, SeatingForm

# Create your views here.

def table_management(request):
    return render(request, 'table-management.html')

# Table views
@login_required
def table(request):
    tables = Table.objects.all()
    return render(request, 'table.html', {'tables': tables})

@login_required
def table_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_waiter):
        raise PermissionDenied
    table = get_object_or_404(Table, id=pk)
    return render(request, 'table-detail.html', {'table': table})

@login_required
def table_add(request):
    if not (request.user.is_admin or request.user.is_manager):
        raise PermissionDenied
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table')
    else:
        form = TableForm()
    return render(request, 'table-add-edit.html', {'form': form})

@login_required
def table_edit(request, pk):
    if not (request.user.is_admin or request.user.is_manager):
        raise PermissionDenied
    table = get_object_or_404(Table, id=pk)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('table')
    else:
        form = TableForm(instance=table)
    return render(request, 'table-add-edit.html', {'form': form})

@login_required
def table_delete(request, pk):
    if not (request.user.is_admin or request.user.is_manager):
        raise PermissionDenied
    table = get_object_or_404(Table, id=pk)
    if request.method == 'POST':
        table.delete()
        return redirect('table')
    return render(request, 'table-delete-confirm.html', {'table': table})

# Reservation views
@login_required
def reservation(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation.html', {'reservations': reservations})

@login_required
def reservation_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_waiter):
        raise PermissionDenied
    reservation = get_object_or_404(Reservation, id=pk)
    return render(request, 'reservation-detail.html', {'reservation': reservation})

@login_required
def reservation_add(request):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.reserved_by = request.user  # Automatically set the logged-in user
            reservation.save()
            return redirect('reservation')
    else:
        form = ReservationForm()
    return render(request, 'reservation-add-edit.html', {'form': form})

@login_required
def reservation_edit(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    reservation = get_object_or_404(Reservation, id=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.reserved_by = request.user  # Automatically set the logged-in user
            reservation.save()
            return redirect('reservation')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation-add-edit.html', {'form': form})

@login_required
def reservation_delete(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    reservation = get_object_or_404(Reservation, id=pk)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation')
    return render(request, 'reservation-delete-confirm.html', {'reservation': reservation})

# Seating views
@login_required
def seating(request):
    seatings = Seating.objects.all()
    return render(request, 'seating.html', {'seatings': seatings})

@login_required
def seating_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_waiter):
        raise PermissionDenied
    seating = get_object_or_404(Seating, id=pk)
    return render(request, 'seating-detail.html', {'seating': seating})

@login_required
def seating_add(request):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    if request.method == 'POST':
        form = SeatingForm(request.POST)
        if form.is_valid():
            seating = form.save(commit=False)
            seating.assigned_by = request.user  # Automatically set the logged-in user
            seating.save()
            return redirect('seating')
    else:
        form = SeatingForm()
    return render(request, 'seating-add-edit.html', {'form': form})

@login_required
def seating_edit(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    seating = get_object_or_404(Seating, id=pk)
    if request.method == 'POST':
        form = SeatingForm(request.POST, instance=seating)
        if form.is_valid():
            seating = form.save(commit=False)
            seating.assigned_by = request.user  # Automatically set the logged-in user
            seating.save()
            return redirect('seating')
    else:
        form = SeatingForm(instance=seating)
    return render(request, 'seating-add-edit.html', {'form': form})

@login_required
def seating_delete(request, pk):
    if not (request.user.is_admin or request.user.is_waiter):
        raise PermissionDenied
    seating = get_object_or_404(Seating, id=pk)
    if request.method == 'POST':
        seating.delete()
        return redirect('seating')
    return render(request, 'seating-delete-confirm.html', {'seating': seating})
