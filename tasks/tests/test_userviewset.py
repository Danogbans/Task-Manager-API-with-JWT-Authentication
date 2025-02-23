import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
class TestUserViewSet:
    """Integration tests for the User API"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data before each test."""
        self.client = APIClient()  # Test client to simulate API requests

    def test_create_user_success(self):
        """Test user registration with valid data."""
        user_data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com"
        }

        response = self.client.post("/api/users/", user_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1  # Ensures user is saved in DB
        assert response.data["username"] == "testuser"
        assert "password" not in response.data  # Password should NOT be exposed

    def test_create_user_validation_error(self):
        """Test user registration with missing required fields."""
        user_data = {
            "username": "testuser"  # Missing 'password' & 'email'
        }

        response = self.client.post("/api/users/", user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data  # Expect validation error
        

    def test_create_user_internal_error(self, mocker):
        """Test handling of unexpected errors (simulated)."""
        mocker.patch("django.contrib.auth.models.User.objects.create_user", side_effect=Exception("DB error"))

        user_data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com"
        }

        response = self.client.post("/api/users/", user_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {"error": "User registration failed"}  # Custom error message