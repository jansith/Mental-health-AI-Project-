from rest_framework import serializers
from .models import AppointmentSlot, Appointment
from project_app.models import DoctorProfile, PatientProfile
from django.utils import timezone
from django.core.exceptions import ValidationError

class AppointmentSlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)

    def validate(self, attrs):
        """
        Validate that end_time is after start_time
        """
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        
        
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time'
            })
        
        # Validate against past dates
        date = attrs.get('date') or (self.instance.date if self.instance else None)
        if date and date < timezone.now().date():
            raise serializers.ValidationError({
                'date': 'Cannot create slots in the past'
            })
        
        return attrs

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
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=DoctorProfile.objects.filter(status='approved')
    )
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

    def validate(self, data):

        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        slot = data.get('slot')

        # Validate date is not in past
        if date and date < timezone.now().date():
            raise serializers.ValidationError({
                'date': 'Cannot book appointments in the past'
            })
        
        # Validate slot availability (optional - if you have slot field)
        slot = data.get('slot')
        if slot:
            if slot.status != 'available':
                raise serializers.ValidationError({
                    'slot': 'This time slot is not available'
                })
            
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time'
            })
        
        if slot:
            if slot.date != date:
                raise serializers.ValidationError({
                    'date' : 'Appointment date must match the slot date'
                })
            elif slot.start_time != start_time or slot.end_time != end_time:
                raise serializers.ValidationError({
                    'time' : 'Appointment timing must match the slot timing'
                })
        
        
        return data
