from django import forms
from user.models import User
from .models import Staff, Shift, LeaveRequest, WorkLog, Resource

#Define form below

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'first_name', 'last_name']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['employee_id', 'address']


class ShiftForm(forms.ModelForm):

    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Shift
        fields = ['name', 'start_time', 'end_time', 'description', 'staff_members']
        widgets = {
            'staff_members': forms.CheckboxSelectMultiple(),  # Use checkboxes for multiple selection
        }

class LeaveRequestForm(forms.ModelForm):

    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']

class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['staff', 'shift', 'clock_in_time', 'clock_out_time']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'file', 'description']
