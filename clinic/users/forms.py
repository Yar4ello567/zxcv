from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import User, Patient, Doctor

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'birth_date']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['insurance_number']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'bio', 'education', 'experience', 'consultation_price']