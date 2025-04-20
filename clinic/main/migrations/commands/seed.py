from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from main.models import User, Specialization, Doctor, Patient, Appointment, Review
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Очистка старых данных
        User.objects.all().delete()
        Specialization.objects.all().delete()
        
        # Создание специализаций
        specializations = [
            'Cardiology',
            'Neurology',
            'Pediatrics',
            'Dermatology',
            'Orthopedics'
        ]
        
        for spec in specializations:
            Specialization.objects.create(
                name=spec,
                description=fake.text()
            )
        
        # Создание администратора
        admin = User.objects.create(
            username='admin',
            email='admin@clinic.com',
            first_name='Admin',
            last_name='User',
            password=make_password('admin123'),
            is_admin=True,
            is_staff=True,
            is_superuser=True
        )
        
        # Создание врачей (15)
        for i in range(1, 16):
            user = User.objects.create(
                username=f'doctor{i}',
                email=f'doctor{i}@clinic.com',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=make_password('doctor123'),
                is_doctor=True,
                phone=fake.phone_number(),
                birth_date=fake.date_of_birth(minimum_age=30, maximum_age=65)
            )
            
            Doctor.objects.create(
                user=user,
                specialization=Specialization.objects.order_by('?').first(),
                bio=fake.text(),
                education=fake.text(),
                experience=random.randint(5, 30),
                consultation_price=random.randint(500, 5000)
            )
        
        # Создание пациентов (30)
        for i in range(1, 31):
            user = User.objects.create(
                username=f'patient{i}',
                email=f'patient{i}@example.com',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=make_password('patient123'),
                is_patient=True,
                phone=fake.phone_number(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=90)
            )
            
            Patient.objects.create(
                user=user,
                insurance_number=fake.uuid4()[:10].upper()
            )
        
        # Создание записей на прием (50)
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()
        
        for i in range(50):
            doctor = random.choice(doctors)
            patient = random.choice(patients)
            
            date = fake.date_between(start_date='-30d', end_date='+30d')
            time = datetime.strptime(f"{random.randint(9, 17)}:{random.choice(['00', '15', '30', '45'])}", "%H:%M").time()
            
            status = random.choices(
                ['scheduled', 'completed', 'canceled'],
                weights=[0.6, 0.3, 0.1]
            )[0]
            
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                date=date,
                time=time,
                status=status,
                reason=fake.sentence()
            )
            
            if status == 'completed':
                appointment.diagnosis = fake.sentence()
                appointment.prescription = fake.text()
                appointment.notes = fake.text()
                appointment.save()
                
                # Создание отзывов для завершенных приемов
                if random.random() > 0.3:  # 70% chance of review
                    Review.objects.create(
                        doctor=doctor,
                        patient=patient,
                        rating=random.randint(1, 5),
                        comment=fake.text()
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))