from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializing the Task model"""

    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }
        

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# Custom JWT Login View: Extends JWT to return extra user details
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Custom JWT Login Serializer to include username & email in response """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data
