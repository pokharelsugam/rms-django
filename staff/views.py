from django.shortcuts import render, get_object_or_404, redirect
from .models import Staff, Shift, LeaveRequest, WorkLog, Resource
from .forms import StaffForm, UserForm, ShiftForm, LeaveRequestForm, ResourceForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


# Create your views here.

def staff_management(request):
    return render(request, 'staff-management.html')

#Staff Management

@login_required
def staff(request):
    staff_objs = Staff.objects.all()
    return render(request, 'staff.html', {'staffs':staff_objs})

@login_required
def staff_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    staff_obj = get_object_or_404(Staff, id=pk)
    return render(request, 'staff-detail.html', {'staff': staff_obj})

@login_required
def staff_edit(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    staff_objs = get_object_or_404(Staff, id=pk)
    user_objs = staff_objs.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user_objs)
        staff_form = StaffForm(request.POST, instance=staff_objs)
        if user_form.is_valid() and staff_form.is_valid():
            user_form.save()
            staff_form.save()
            return redirect('staff_detail', pk=staff_objs.id)
    else:
        user_form = UserForm(instance=user_objs)
        staff_form = StaffForm(instance=staff_objs)
    return render(request, 'staff-edit.html', {'user_form': user_form, 'staff_form': staff_form})

@login_required
def staff_delete(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    staff_objs = get_object_or_404(Staff, id=pk)
    if request.method == 'POST':
        user_objs = staff_objs.user
        staff_objs.delete()
        user_objs.delete()
        return redirect('staff')
    return render(request, 'staff-delete-confirm.html', {'staff': staff_objs})


#Shift Management

@login_required
def shift(request):
    shift_objs = Shift.objects.all()
    return render(request, 'shift.html', {'shifts': shift_objs})

@login_required
def shift_detail(request, pk):
    shift_obj = get_object_or_404(Shift, id=pk)
    return render(request, 'shift-detail.html', {'shift': shift_obj})

@login_required
def shift_create(request):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save()
            return redirect('shift')
    else:
        form = ShiftForm()
    return render(request, 'shift-create-edit.html', {'form': form})

@login_required
def shift_edit(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    shift_obj = get_object_or_404(Shift, id=pk)
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift_obj)
        if form.is_valid():
            form.save()
            return redirect('shift')
    else:
        form = ShiftForm(instance=shift_obj)
    return render(request, 'shift-create-edit.html', {'form': form})

@login_required
def shift_delete(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    shift = get_object_or_404(Shift, id=pk)
    if request.method == 'POST':
        shift.delete()
        return redirect('shift')
    return render(request, 'shift-delete-confirm.html', {'shift': shift})

@login_required
def leave_request(request):
    leave_request_objs = LeaveRequest.objects.all()
    return render(request, 'leave-request.html', {'leave_requests': leave_request_objs})

@login_required
def leave_req_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    leave_request_obj = get_object_or_404(LeaveRequest, id=pk)
    return render(request, 'leave-req-detail.html', {'leave_request': leave_request_obj})

@login_required
def leave_req_create(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            try:
                leave_request.staff = request.user.staff  # Assuming staff association based on logged-in user
            except:
                return HttpResponse('You are not a staff you are just user please try again from staff account. If you are a staff please request to admin to assign your user account in staff from Django Admin pannel')    
            leave_request.request_date = timezone.now().date()  # Set request_date to the current date
            leave_request.save()
            return redirect('leave_request')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave-req-create.html', {'form': form})

@login_required
def leave_req_delete(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    leave_request_obj = get_object_or_404(LeaveRequest, id=pk)
    if request.method == 'POST':
        leave_request_obj.delete()
        return redirect('leave_request')
    return render(request, 'leave-req-delete-confirm.html', {'leave_request': leave_request_obj})

@login_required
def leave_req_approve(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    leave_request_obj = get_object_or_404(LeaveRequest, id=pk)
    if request.method == 'POST':
        # Handle approval logic, update status, set approved_by, etc.
        leave_request_obj.leave_req_status = 'AP'
        leave_request_obj.approved_by = request.user
        leave_request_obj.save()
        return redirect('leave_request')
    return render(request, 'leave-req-approve.html', {'leave_request': leave_request_obj})

@login_required
def leave_req_reject(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    leave_request_obj = get_object_or_404(LeaveRequest, id=pk)
    if request.method == 'POST':
        # Handle rejection logic, update status, etc.
        leave_request_obj.leave_req_status = 'RJ'
        leave_request_obj.approved_by = request.user
        leave_request_obj.save()
        return redirect('leave_request')
    return render(request, 'leave-req-reject.html', {'leave_request': leave_request_obj})

@login_required
def worklog(request):
    worklog_objs = WorkLog.objects.all()
    return render(request, 'worklog.html', {'worklogs': worklog_objs})

@login_required
def worklog_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    worklog_obj = get_object_or_404(WorkLog, id=pk)
    return render(request, 'worklog-detail.html', {'worklog': worklog_obj})

@login_required
def worklog_create(request):
    current_time = timezone.now()  # UTC time
    try:
        staff = request.user.staff
    except:
        return HttpResponse('You are not a staff you are just user please try again from staff account. If you are a staff please request to admin to assign your user account in staff from Django Admin pannel')   

    # Find the active shift for the current time
    active_shifts = Shift.objects.filter(staff_members = staff, start_time__lte=current_time.time(), end_time__gte=current_time.time())

    if not active_shifts.exists():
        # Handle the case where no active shift is found
        return render(request, 'worklog-create.html', {
            'error': 'No active shift found for the current time and current user.',
            'staff': staff,
            'full_name': request.user.get_full_name(),
            'current_time': current_time,
        })

    # Assume that we only want to use the first active shift for simplicity
    active_shift = active_shifts.first()

    # Check if there's already an active work log entry
    existing_work_log = WorkLog.objects.filter(staff=staff, shift=active_shift, clock_out_time__isnull=True).first()

    if request.method == 'POST':
        if 'clock_in' in request.POST:
            if existing_work_log:
                return render(request, 'worklog-create.html', {
                    'error': 'You are already clocked in.',
                    'staff': staff,
                    'current_shift': active_shift,
                    'full_name': request.user.get_full_name(),
                    'current_time': current_time,
                })

            # Create a new work log entry for clock-in
            worklog = WorkLog(
                staff=staff,
                shift=active_shift,
                clock_in_time=current_time
            )
            worklog.save()
            return redirect('worklog')

        elif 'clock_out' in request.POST:
            if not existing_work_log:
                return render(request, 'worklog-create.html', {
                    'error': 'No active clock-in entry found.',
                    'staff': staff,
                    'current_shift': active_shift,
                    'full_name': request.user.get_full_name(),
                    'current_time': current_time,
                })

            # Update existing work log entry with clock-out time
            existing_work_log.clock_out_time = current_time
            existing_work_log.save()
            return redirect('worklog')

    return render(request, 'worklog-create.html', {
        'staff': staff,
        'current_shift': active_shift,
        'existing_work_log': existing_work_log,
        'error': None,
        'full_name': request.user.get_full_name(),
        'current_time': current_time,
    })

@login_required
def worklog_delete(request, pk):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    worklog_obj = get_object_or_404(WorkLog, id=pk)
    if request.method == 'POST':
        worklog_obj.delete()
        return redirect('worklog')
    return render(request, 'worklog-delete-confirm.html', {'worklog': worklog_obj})


@login_required
def resource(request):
    resources = Resource.objects.all()
    return render(request, 'resource.html', {'resources': resources})


@login_required
def resource_get(request, pk):
    resource_obj = get_object_or_404(Resource, id=pk)
    return render(request, 'resource-get.html', {'resource': resource_obj})

@login_required
def resource_add(request):
    if not (request.user.is_admin or request.user.is_manager):
        raise PermissionDenied('Please login with admin or manager account')
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('resource')
    else:
        form = ResourceForm()
    return render(request, 'resource-add-edit.html', {'form': form})

@login_required
def resource_edit(request, pk):
    if not (request.user.is_admin or request.user.is_manager):
        raise PermissionDenied('Please login with admin or manager account')
    resource = get_object_or_404(Resource, id=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resource-add-edit.html', {'form': form})

@login_required
def resource_delete(request, pk):
    if not (request.user.is_admin or request.user.is_manager):
        raise PermissionDenied('Please login with admin or manager account')
    resource = get_object_or_404(Resource, id=pk)
    if request.method == 'POST':
        resource.delete()
        return redirect('resource')
    return render(request, 'resource-delete-confirm.html', {'resource': resource})