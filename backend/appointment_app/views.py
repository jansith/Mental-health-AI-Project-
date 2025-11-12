from django.shortcuts import render
from rest_framework.views import APIView,status
from .models import *
from .serializer import *
from rest_framework.response import Response

# Create your views here.

class AppoinmentSlotApi(APIView):

    def post(self, request):
        serializer = AppointmentSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Slot created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Slot creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
        try:
            slots = AppointmentSlot.objects.all()
            serializer = AppointmentSlotSerializer(slots, many=True)
            return Response({
                'status': 'success',
                'message': 'Docters slots data retrieved successfully',
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve doctors slots  data',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentApi(APIView):
    
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Appointment created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Appointment creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            appointments = Appointment.objects.all()
            serializer = AppointmentSerializer(appointments, many=True)

            return Response({
                'status': 'success',
                'message': 'Appointments data retrieved successfully',
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve appointments data',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            