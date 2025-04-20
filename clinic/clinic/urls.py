from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from appointments import views as appointment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', appointment_views.home, name='home'),
    
    # Auth URLs
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    
    # Appointment URLs
    path('appointments/', appointment_views.appointments_list, name='appointments'),
    path('appointments/<int:pk>/', appointment_views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/pdf/', appointment_views.generate_pdf, name='generate_pdf'),
    path('appointments/book/', appointment_views.book_appointment, name='book_appointment'),
    
    # Doctor URLs
    path('doctors/', appointment_views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', appointment_views.doctor_detail, name='doctor_detail'),
]