from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Specialization, Doctor, Patient, Appointment, Review

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_patient', 'is_doctor', 'is_admin')
    list_filter = ('is_patient', 'is_doctor', 'is_admin')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_patient', 'is_doctor', 'is_admin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience', 'consultation_price')
    list_filter = ('specialization',)
    search_fields = ('user__first_name', 'user__last_name')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'insurance_number')
    search_fields = ('user__first_name', 'user__last_name')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor__specialization')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    date_hierarchy = 'date'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'created_at')
    list_filter = ('rating', 'doctor__specialization')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name', 'patient__user__first_name', 'patient__user__last_name')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Specialization)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Review, ReviewAdmin)