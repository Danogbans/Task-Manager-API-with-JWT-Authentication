import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
class TestTaskViewSet:
    """Tests for the TaskViewSet API endpoint."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data and authentication before each test."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)

        # Create sample tasks for filtering
        self.task1 = Task.objects.create(
            title="Pending Task", status="Pending", priority=2, assigned_to=self.user
        )
        self.task2 = Task.objects.create(
            title="Completed Task", status="Completed", priority=1, assigned_to=self.user
        )


    def test_create_task_success(self):
        """Test creating a task with valid data."""
        task_data = {
            "title": "New Task",
            "status": "Pending",
            "priority": 3,
            "assigned_to": self.user.id,
        }

        response = self.client.post("/api/tasks/", task_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 3  # Two pre-existing + one new task
        assert response.data["title"] == "New Task"


    def test_create_task_validation_error(self):
        """Test task creation with missing required fields."""
        task_data = {
            "status": "Pending"  # Missing 'title' and 'assigned_to'
        }

        response = self.client.post("/api/tasks/", task_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data  # Expect title to be required
        assert "assigned_to" in response.data  # Expect assigned_to to be required


    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status."""
        response = self.client.get("/api/tasks/?status=Pending")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1  # Only 1 task should have status=Pending
        assert response.data["results"][0]["title"] == "Pending Task"


    def test_filter_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        response = self.client.get("/api/tasks/?priority=1")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1  # Only 1 task should have priority=1
        assert response.data["results"][0]["title"] == "Completed Task" 


    def test_authentication_required(self):
        """Test that authentication is required to access the API."""
        client = APIClient()  # New unauthenticated client
        response = client.get("/api/tasks/")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]