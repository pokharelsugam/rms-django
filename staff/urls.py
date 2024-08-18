from django.urls import path
from .views import staff_management,staff, staff_detail, staff_edit, staff_delete, shift, shift_detail, shift_create, shift_edit, shift_delete, leave_request, leave_req_detail, leave_req_create, leave_req_delete, leave_req_approve,leave_req_reject, worklog,worklog_detail,worklog_create,worklog_delete, resource, resource_get, resource_add, resource_edit, resource_delete

urlpatterns = [
    path('', staff_management, name='staff_management'),
    # Staff Urls
    path('member/', staff, name='staff'),
    path('member/<int:pk>/', staff_detail, name='staff_detail'),
    path('member/edit/<int:pk>/', staff_edit, name='staff_edit'),
    path('member/delete/<int:pk>/', staff_delete, name='staff_delete'),
    # Shift Urls
    path('shift/', shift, name='shift'),
    path('shift/create/', shift_create, name='shift_create'),
    path('shift/<int:pk>/', shift_detail, name='shift_detail'),
    path('shift/edit/<int:pk>/',shift_edit, name='shift_edit'),
    path('shift/delete/<int:pk>/',shift_delete, name='shift_delete'),

    # Leave Urls
    path('leave-request/', leave_request, name='leave_request'),
    path('leave-request/<int:pk>/', leave_req_detail, name='leave_req_detail'),
    path('leave-request/create/', leave_req_create, name='leave_req_create'),
    path('leave-request/delete/<int:pk>/', leave_req_delete, name = 'leave_req_delete'),
    path('leave-request/approve/<int:pk>/', leave_req_approve, name='leave_req_approve'),
    path('leave-request/reject/<int:pk>/', leave_req_reject, name='leave_req_reject'),

    # WorkLog URLs
    path('worklog/', worklog, name='worklog'),
    path('worklog/<int:pk>/', worklog_detail, name='worklog_detail'),
    path('worklog/create/', worklog_create, name='worklog_create'),
    path('worklog/delete/<int:pk>/', worklog_delete, name='worklog_delete'),

    # Resource Urls
    path('resource/', resource, name='resource'),
    path('resource/<int:pk>/', resource_get, name='resource_get'),
    path('resource/add/', resource_add, name='resource_add'),
    path('resource/edit/<int:pk>/', resource_edit, name='resource_edit'),
    path('resource/delete/<int:pk>/', resource_delete, name='resource_delete'),
]

# Resource file url is in RMS/urls.py