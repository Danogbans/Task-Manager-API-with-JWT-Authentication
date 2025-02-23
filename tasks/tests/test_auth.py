import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status



@pytest.mark.django_db
class TestCustomLoginView:
    """Integration tests for JWT login with custom serializer"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test user before each test."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="testuser@example.com")

    def test_jwt_login_success(self):
        """Test successful JWT login returns tokens and user details."""
        login_data = {
            "username": "testuser",
            "password": "password123"
        }

        response = self.client.post("/api/token/", login_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data  
        assert "refresh" in response.data  
        assert response.data["username"] == "testuser"  
        assert response.data["email"] == "testuser@example.com"  

    def test_jwt_login_invalid_credentials(self):
        """Test login with incorrect credentials returns 401."""
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }

        response = self.client.post("/api/token/", login_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "access" not in response.data  #  No token should be returned
        assert "refresh" not in response.data  #  No token should be returned
        assert "username" not in response.data  #  Custom field should be absent
        assert "email" not in response.data  #  Custom field should be absent