from django.contrib.auth import get_user_model
from rest_framework.serializers import  CharField, EmailField
from rest_framework import serializers
from .models import Notes

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
    
