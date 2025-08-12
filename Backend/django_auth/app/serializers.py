from django.contrib.auth import get_user_model
from rest_framework.serializers import  CharField, EmailField
from rest_framework import serializers
from .models import Notes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = CharField(write_only=True)
    email = EmailField(required=True)
    class Meta:
        model = get_user_model()
        fields = ['username','email','password']
        
    def create(self,validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email = validated_data['email'],
            password= validated_data['password'],
        )
        return user

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        
        
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):   
    email = serializers.EmailField(required=True)
    password = CharField(write_only=True)
    
    def validate(self, attrs):
        credentials = {
              'email' : attrs.get("email"),
              'password' : attrs.get('password')
          }
        user = get_user_model().objects.filter(email=credentials['email']).first()
        if user is None :
            raise serializers.ValidationError('No active account found with the given credentials')
        if not user.check_password(credentials['password']):
            raise serializers.ValidationError("Wrong email or password")
        
        data = super().validate({
            'username': user.username,
            'password': credentials['password']
        })
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
    