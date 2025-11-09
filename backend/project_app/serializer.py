from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm Password'
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password', 'password2', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Validate role
        valid_roles = ['patient', 'doctor', 'admin']
        if attrs.get('role') not in valid_roles:
            raise serializers.ValidationError({"role": f"Role must be one of {valid_roles}"})
            
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('Account disabled')
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Must include email and password')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'role', 'is_active', 'created_at')
        read_only_fields = ('id', 'is_active', 'created_at')

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='doctor'), 
        write_only=True,
        source='user'
    )
    
    class Meta:
        model = DoctorProfile
        fields = '__all__'
        read_only_fields = ('status',)

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='patient'), 
        write_only=True,
        source='user'
    )
    
    class Meta:
        model = PatientProfile
        fields = '__all__'

# class DoctorProfileCreateSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(write_only=True)
#     full_name = serializers.CharField(write_only=True)
#     password = serializers.CharField(write_only=True)
    
#     class Meta:
#         model = DoctorProfile
#         exclude = ('user', 'status')
        
    # def create(self, validated_data):
    #     # This would be handled in the view
    #     pass 