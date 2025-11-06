from django.shortcuts import render
from rest_framework.views import APIView,status
from .models import *
from .serializer import *
from rest_framework.response import Response

# Create your views here.
class CreateUserApi(APIView):
   
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create profile based on role
            if user.role == 'doctor':
                DoctorProfile.objects.create(user=user)
            elif user.role == 'patient':
                PatientProfile.objects.create(user=user)
            
            # Return user data without password
            user_serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'message': 'User created successfully',
                'data': user_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'User creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({
                'status': 'success',
                'message': 'Users data retrieved successfully',
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve users data',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            response_data = {
                "user_id": user.pk,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role
            }
            
            # Add profile information based on role
            if user.role == 'doctor' and hasattr(user, 'doctor_profile'):
                response_data['profile_status'] = user.doctor_profile.status
            elif user.role == 'patient' and hasattr(user, 'patient_profile'):
                response_data['patient_id'] = user.patient_profile.patient_id
            
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': response_data
            })
        
        return Response({
            'status': 'error',
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class DoctorProfileApi(APIView):
    
    def post(self, request):
        if request.user.role != 'doctor':
            return Response({
                'status': 'error',
                'message': 'Only doctors can create doctor profiles'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if profile already exists
        if hasattr(request.user, 'doctor_profile'):
            return Response({
                'status': 'error',
                'message': 'Doctor profile already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DoctorProfileSerializer(data=request.data)
        if serializer.is_valid():
            # Associate with current user
            serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'message': 'Doctor profile created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Doctor profile creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Get doctor profile"""
        if not hasattr(request.user, 'doctor_profile'):
            return Response({
                'status': 'error',
                'message': 'Doctor profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DoctorProfileSerializer(request.user.doctor_profile)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

class PatientProfileApi(APIView): 
    
    def post(self, request):
        
        if request.user.role != 'patient':
            return Response({
                'status': 'error',
                'message': 'Only patients can create patient profiles'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if profile already exists
        if hasattr(request.user, 'patient_profile'):
            return Response({
                'status': 'error',
                'message': 'Patient profile already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PatientProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'message': 'Patient profile created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Patient profile creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        
        if not hasattr(request.user, 'patient_profile'):
            return Response({
                'status': 'error',
                'message': 'Patient profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientProfileSerializer(request.user.patient_profile)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
class DoctorApprovalAPIView(APIView):

    def patch(self, request, id):
        doctor_profile = DoctorProfile.objects.get(id=id)
        new_status = request.data.get('status')
        
        if new_status not in ['approved', 'rejected']:
            return Response({
                'status': 'error',
                'message': 'Status must be either "approved" or "rejected"'
            }, status=status.HTTP_400_BAD_REQUEST)

        doctor_profile.status = new_status
        doctor_profile.save()
        
        serializer = DoctorProfileSerializer(doctor_profile)
        return Response({
            'status': 'success',
            'message': f'Doctor profile {new_status} successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
