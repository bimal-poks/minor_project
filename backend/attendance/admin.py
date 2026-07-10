from django.contrib import admin
from .models import Student, FaceEmbedding, Session, AttendanceRecord

admin.site.register(Student)
admin.site.register(FaceEmbedding)
admin.site.register(Session)
admin.site.register(AttendanceRecord)
