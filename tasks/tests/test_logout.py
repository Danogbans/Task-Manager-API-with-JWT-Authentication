import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from tasks.utils import logout_user



@pytest.mark.django_db
class TestLogoutUser:
    """Integration tests for the logout function and LogoutView API."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test user and authentication before each test."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="testuser@example.com")
        self.refresh = str(RefreshToken.for_user(self.user))  # Generate a valid refresh token
        self.access = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")  # Authenticate user

    def test_logout_success(self):
        """Test successful logout blacklists the refresh token."""
        logout_data = {"refresh": self.refresh}  # Provide valid refresh token
        response = self.client.post("/api/logout/", logout_data, format="json")

        assert response.status_code == status.HTTP_205_RESET_CONTENT
        assert response.data["message"] == "Logged out successfully"

    def test_logout_missing_token(self):
        """Test logout fails when no refresh token is provided."""
        logout_data = {}  # No refresh token
        response = self.client.post("/api/logout/", logout_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Refresh token required"

    def test_logout_invalid_token(self):
        """Test logout fails when an invalid refresh token is provided."""
        logout_data = {"refresh": "invalidtoken123"}  #  Invalid token
        response = self.client.post("/api/logout/", logout_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid token"