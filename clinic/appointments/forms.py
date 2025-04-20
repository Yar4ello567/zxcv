from django import forms
from main.models import User, Patient, Doctor, Appointment, Review, Specialization
from django.utils import timezone
import datetime

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        initial=datetime.time(9, 0)
    )
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("You cannot book an appointment in the past.")
        return date

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['diagnosis', 'prescription', 'notes', 'status']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }