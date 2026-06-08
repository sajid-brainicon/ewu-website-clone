from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'program', 'semester', 'year', 'is_verified', 'created_at')
    list_filter = ('program', 'semester', 'is_verified', 'year')
    search_fields = ('student_id', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'student_id', 'program', 'semester', 'year')
        }),
        ('Contact & Personal', {
            'fields': ('phone', 'date_of_birth', 'address', 'profile_pic')
        }),
        ('Status', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )