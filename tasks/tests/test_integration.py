import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from tasks.models import Task
from django.core import mail
from unittest.mock import patch
from django.conf import settings


@pytest.mark.django_db
class TestTaskManagerAPI:
    """Integration Test for Task Management API"""

    def setup_method(self):
        """Setup method to create test client and user."""
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_full_task_lifecycle(self):
        """Test full task lifecycle: user registration, login, task creation, retrieval, and logout."""

        # Step 1: Registering a new user
        response = self.client.post("/api/users/", self.user_data, format="json")
        assert response.status_code in [201, 400]  # 201: Created, 400: Already exists

        # Step 2: Logging in to obtain JWT token
        login_data = {"username": "testuser", "password": "password123"}
        response = self.client.post("/api/token/", login_data, format="json")
        assert response.status_code == 200
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        # Step 3: Using token for authentication
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Step 4: Create a task
        task_data = {
            "title": "Integration Test Task",
            "status": "Pending",
            "priority": 2,
            "assigned_to": self.user.id,
        }
        response = self.client.post("/api/tasks/", task_data, format="json")
        assert response.status_code == 201
        task_id = response.data["id"]

        # Step 5: Retrieve the created task
        response = self.client.get(f"/api/tasks/{task_id}/")
        assert response.status_code == 200
        assert response.data["title"] == "Integration Test Task"

        # Step 6: Test signal (email sent on task creation)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["testuser@example.com"]
        assert "New Task Assigned" in mail.outbox[0].subject

        # Step 7: Test logout
        response = self.client.post("/api/logout/", {"refresh": refresh_token}, format="json")
        print("Logout Response:", response.json()) 
        assert response.status_code == 205  # Token should be blacklisted