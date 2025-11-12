from rest_framework import serializers
from .models import AppointmentSlot, Appointment
from project_app.models import DoctorProfile, PatientProfile

class AppointmentSlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)

    class Meta:
        model = AppointmentSlot
        fields = [
            'id', 'doctor', 'doctor_name', 'doctor_specialization', 
            'date', 'start_time', 'end_time', 'status', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)
    slot_info = serializers.CharField(source='slot.__str__', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'appointment_id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'slot', 'slot_info', 'date', 'start_time', 'end_time', 'status',
            'reason', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['appointment_id', 'created_at', 'updated_at']
