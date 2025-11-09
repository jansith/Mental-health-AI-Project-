from django.db import models
from project_app.models import *

# Create your models here.

class AppointmentSlot(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('booking_full', 'Booking full'),
    )
    
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointment_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.date} {self.start_time.strftime('%H:%M')}"


def generate_appointment_id():
    return f"APT{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    appointment_id = models.CharField(max_length=20, unique=True, default=generate_appointment_id, editable=False)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name='appointment')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.patient.user.full_name} with Dr. {self.doctor.user.full_name}"

