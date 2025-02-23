from .models import Task
from django.contrib.auth.models import User
from .serializers import TaskSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from .utils import logout_user

     

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Tasks.
    """

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'assigned_to']

    
    def create(self, request, *args, **kwargs):
        """Handles task creation with error handling."""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Task creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Public registration allowed

    def create(self, request, *args, **kwargs):
        """Handles user registration with error handling."""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "User registration failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomLoginView(TokenObtainPairView):
    """ JWT-based login view that includes extra user details """
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """Handles user logout using the utility function"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        return logout_user(request) 