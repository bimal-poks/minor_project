from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentListCreateView.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('sessions/', views.SessionListCreateView.as_view(), name='session-list'),
    path('attendance/mark/', views.mark_attendance, name='mark-attendance'),
    path('attendance/report/', views.attendance_report, name='attendance-report'),
    path('attendance/today/', views.today_summary, name='today-summary'),
    path('attendance/export/', views.export_attendance_csv, name='export-csv'),
    path('auth/login/', views.login_view, name='login'),
]