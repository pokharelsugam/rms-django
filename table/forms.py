from django import forms
from .models import Table, Reservation, Seating

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_number', 'capacity', 'table_status']

class ReservationForm(forms.ModelForm):

    reservation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Reservation
        fields = ['table', 'reservation_date', 'start_time','end_time','guest_name', 'guest_count']

class SeatingForm(forms.ModelForm):

    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Seating
        fields = ['table', 'guest_name', 'guest_count', 'start_time', 'end_time']
