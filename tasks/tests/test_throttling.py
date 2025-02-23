import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status



@pytest.mark.django_db
class TestAPIThrottling:
    """Tests API request throttling for anonymous and authenticated users."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up API client and test user."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)  #  Simulate an authenticated user

    
    def test_anon_user_throttling(self):
        """Test that anonymous users are throttled after 10 requests/min."""
        for i in range(10):  #  Make 10 successful requests
            response = self.client.get("/api/tasks/")
            assert response.status_code == status.HTTP_200_OK

        response = self.client.get("/api/tasks/")  #  11th request should fail
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Request was throttled" in response.data["detail"]


    def test_authenticated_user_throttling(self):
        """Test that authenticated users are throttled after 50 requests/min."""
        for i in range(50):  #  Make 50 successful requests
            response = self.authenticated_client.get("/api/tasks/")
            assert response.status_code == status.HTTP_200_OK

        response = self.authenticated_client.get("/api/tasks/")  #  51st request should fail
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Request was throttled" in response.data["detail"]