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
            serializer.save()
            
            return Response({
                'status': 'success',
                'message': 'User created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'User creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            serializer = RegisterUserSerializer(users, many=True)
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
        # if request.user.role != 'doctor':
        #     return Response({
        #         'status': 'error',
        #         'message': 'Only doctors can create doctor profiles'
        #     }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if profile already exists
        if hasattr(request.user, 'doctor_profile'):
            return Response({
                'status': 'error',
                'message': 'Doctor profile already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DoctorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # serializer.save(user=request.user)
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
    
    def get(self, request, id=None):
        try:

            if id is not None:
                doctor_profile = DoctorProfile.objects.get(id=id)
                serializer = DoctorProfileSerializer(doctor_profile)
                return Response({
                    'status': 'success',
                    'message': 'Doctor profile retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            
            doctor_profiles = DoctorProfile.objects.all()
            serializer = DoctorProfileSerializer(doctor_profiles, many=True)
            return Response({
                'status': 'success',
                'message': 'Doctor profiles retrieved successfully',
                'data': serializer.data,
                'count': len(serializer.data)  
            }, status=status.HTTP_200_OK)
        
        except DoctorProfile.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Doctor profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve doctor profiles',
                'error': str(e)  
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id):
        try:
            doctorprofile = DoctorProfile.objects.get(id=id)
            serializer = DoctorProfileSerializer(doctorprofile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 'success',
                    'message' : 'Doctor profle details edtied sucessfully',
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 'error',
                'message': 'Doctor profile details editing failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except DoctorProfile.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Doctor profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        doctorprofile = DoctorProfile.objects.get(id=id)
        doctorprofile.delete()
        return Response({
            'status' : 'success',
            'message' : 'doctor details deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
        
class PatientProfileApi(APIView): 
    
    def post(self, request):
        
        # if request.user.role != 'patient':
        #     return Response({
        #         'status': 'error',
        #         'message': 'Only patients can create patient profiles'
        #     }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if profile already exists
        if hasattr(request.user, 'patient_profile'):
            return Response({
                'status': 'error',
                'message': 'Patient profile already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PatientProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
    
    def get(self, request, id=None):
        try:
            
            if id is not None:
                patient_profile = PatientProfile.objects.get(id=id)
                serializer = PatientProfileSerializer(patient_profile)
                return Response({
                    'status': 'success',
                    'message': 'Patient profile retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            
            patient_profiles = PatientProfile.objects.all()
            serializer = PatientProfileSerializer(patient_profiles, many=True)
            return Response({
                'status': 'success',
                'message': 'Patient profiles retrieved successfully',
                'data': serializer.data,
                'count': len(serializer.data)  
            }, status=status.HTTP_200_OK)
        
        except PatientProfile.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Patient profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve patient profiles',
                'error': str(e)  
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id):
        try:
            patientProfile = PatientProfile.objects.get(id=id)
            serializer = PatientProfileSerializer(patientProfile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 'success',
                    'message' : 'Patient profle details edtied sucessfully',
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 'error',
                'message': 'Patient profile details editing failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except PatientProfile.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'patient profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        patientprofile = PatientProfile.objects.get(id=id)
        patientprofile.delete()
        return Response({
            'status' : 'success',
            'message' : 'patient details deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
class DoctorApprovalAPIView(APIView):

    def patch(self, request, id):
        try:
            doctor_profile = DoctorProfile.objects.get(id=id)
        except DoctorProfile.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Doctor profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user has permission to approve doctors
        if not request.user.is_staff and request.user.role != 'admin':
            return Response({
                'status': 'error',
                'message': 'Only admin users can approve doctors'
            }, status=status.HTTP_403_FORBIDDEN)

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