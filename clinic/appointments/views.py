from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from reportlab.pdfgen import canvas
from io import BytesIO
from .forms import AppointmentForm, ReviewForm, AppointmentUpdateForm
from main.models import Appointment, Doctor, Review, Specialization
import datetime

def home(request):
    return render(request, 'home.html')

@login_required
def book_appointment(request):
    if not request.user.is_patient:
        messages.warning(request, 'Only patients can book appointments.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            messages.success(request, 'Your appointment has been booked!')
            return redirect('appointments')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book.html', {'form': form})

@login_required
def appointments_list(request):
    if request.user.is_patient:
        appointments = Appointment.objects.filter(patient=request.user.patient).order_by('-date', '-time')
    elif request.user.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user.doctor).order_by('-date', '-time')
    else:
        appointments = Appointment.objects.none()
    
    return render(request, 'appointments/list.html', {'appointments': appointments})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Проверка доступа
    if not (request.user == appointment.patient.user or request.user == appointment.doctor.user or request.user.is_admin):
        messages.warning(request, 'You are not authorized to view this appointment.')
        return redirect('home')
    
    if request.method == 'POST' and (request.user.is_doctor or request.user.is_admin):
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('appointment_detail', pk=pk)
    else:
        form = AppointmentUpdateForm(instance=appointment)
    
    return render(request, 'appointments/detail.html', {
        'appointment': appointment,
        'form': form if (request.user.is_doctor or request.user.is_admin) else None
    })

@login_required
def doctor_list(request):
    specializations = Specialization.objects.all()
    selected_spec = request.GET.get('specialization')
    
    if selected_spec:
        doctors = Doctor.objects.filter(specialization_id=selected_spec)
    else:
        doctors = Doctor.objects.all()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('appointments/partials/doctor_list.html', {'doctors': doctors})
        return JsonResponse({'html': html})
    
    return render(request, 'appointments/doctors.html', {
        'doctors': doctors,
        'specializations': specializations,
        'selected_spec': selected_spec
    })

@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    reviews = doctor.reviews.all()
    
    if request.method == 'POST' and request.user.is_patient:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.doctor = doctor
            review.patient = request.user.patient
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('doctor_detail', pk=pk)
    else:
        review_form = ReviewForm()
    
    # Проверяем, оставлял ли текущий пользователь отзыв
    user_review = None
    if request.user.is_authenticated and request.user.is_patient:
        user_review = Review.objects.filter(doctor=doctor, patient=request.user.patient).first()
    
    return render(request, 'appointments/doctor_detail.html', {
        'doctor': doctor,
        'reviews': reviews,
        'review_form': review_form if request.user.is_patient and not user_review else None,
        'user_review': user_review
    })

@login_required
def generate_pdf(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.user != appointment.patient.user and not request.user.is_admin:
        messages.warning(request, 'You are not authorized to view this certificate.')
        return redirect('home')
    
    # Создаем PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Заголовок
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Medical Certificate")
    p.line(100, 795, 500, 795)
    
    # Информация о пациенте
    p.setFont("Helvetica", 12)
    p.drawString(100, 760, f"Patient: {appointment.patient.user.get_full_name()}")
    p.drawString(100, 740, f"Date of Birth: {appointment.patient.user.birth_date}")
    p.drawString(100, 720, f"Insurance Number: {appointment.patient.insurance_number}")
    
    # Информация о приеме
    p.drawString(100, 680, f"Doctor: {appointment.doctor.user.get_full_name()}")
    p.drawString(100, 660, f"Specialization: {appointment.doctor.specialization}")
    p.drawString(100, 640, f"Appointment Date: {appointment.date} at {appointment.time}")
    
    # Диагноз и назначения
    p.drawString(100, 600, "Diagnosis:")
    p.drawString(120, 580, appointment.diagnosis if appointment.diagnosis else "Not specified")
    
    p.drawString(100, 540, "Prescription:")
    p.drawString(120, 520, appointment.prescription if appointment.prescription else "Not specified")
    
    # Подпись и дата
    p.drawString(100, 460, f"Date of Issue: {timezone.now().date()}")
    p.drawString(350, 460, "Signature: ___________________")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="medical_certificate_{appointment.id}.pdf"'
    return response