from django.contrib import admin
from .models import Staff, Shift, LeaveRequest,Resource, WorkLog

# Register your models here.

admin.site.register(Staff)
admin.site.register(Shift)
admin.site.register(LeaveRequest)
admin.site.register(Resource)
admin.site.register(WorkLog)