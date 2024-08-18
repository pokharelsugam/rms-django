from django.db import models
from user.models import User
import os

# Create your models here.


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=255)  # Increased length for more detailed addresses

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.employee_id})'


class Shift(models.Model):
    name = models.CharField(max_length=16)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    staff_members = models.ManyToManyField(Staff, blank=True, related_name='shifts')

    def __str__(self):
        return f'{self.name} ({self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")})'


class LeaveRequest(models.Model):
    LEAVE_REQ_STATUS_CHOICES = [
        ('PN', 'Pending'),
        ('AP', 'Approved'),
        ('RJ', 'Rejected'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    request_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    leave_req_status = models.CharField(max_length=2, choices=LEAVE_REQ_STATUS_CHOICES, default='PN')
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='handled_approvals')

    class Meta:
        unique_together = ['staff', 'start_date', 'end_date']

    def __str__(self):
        leave_req_status_display = dict(self.LEAVE_REQ_STATUS_CHOICES).get(self.leave_req_status, 'Unknown')
        return f'{self.staff.user.get_full_name()} ({leave_req_status_display})'    


class WorkLog(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='work_logs')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='work_logs')
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(blank=True, null=True)

    @property
    def hours_worked(self):
        if self.clock_out_time:
            return (self.clock_out_time - self.clock_in_time).total_seconds() / 3600
        return 0
    
    def __str__(self):
        # Extract the date and time from clock_in_time
        clock_in_date = self.clock_in_time.date().strftime('%Y-%m-%d')
        clock_in_time = self.clock_in_time.time().strftime('%H:%M:%S')
        return f'{self.staff.user.username} ({clock_in_date} - {clock_in_time})'
    

class Resource(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    description = models.TextField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Check if we are updating an existing instance
        if self.pk:
            try:
                old_file = Resource.objects.get(pk=self.pk).file
            except Resource.DoesNotExist:
                old_file = None

            if old_file and old_file != self.file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)

        super().save(*args, **kwargs)




# This code only delete file from local directory while deleting resource not delete old file while updating

    # def delete(self, *args, **kwargs): 
    #     if self.file:
    #         if os.path.isfile(self.file.path):
    #             os.remove(self.file.path) 
    #     super().delete(*args, **kwargs)