from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, PatientProfileForm, DoctorProfileForm
from main.models import Patient, Doctor

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True  # По умолчанию регистрируем как пациента
            user.save()
            Patient.objects.create(user=user)
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if request.user.is_patient:
            p_form = PatientProfileForm(request.POST, instance=request.user.patient)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your account has been updated!')
                return redirect('profile')
        elif request.user.is_doctor:
            p_form = DoctorProfileForm(request.POST, instance=request.user.doctor)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your account has been updated!')
                return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        if request.user.is_patient:
            p_form = PatientProfileForm(instance=request.user.patient)
        elif request.user.is_doctor:
            p_form = DoctorProfileForm(instance=request.user.doctor)
        else:
            p_form = None
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/profile.html', context)