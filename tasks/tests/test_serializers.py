import pytest
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework.exceptions import ValidationError
from tasks.serializers import TaskSerializer
from tasks.models import Task


@pytest.mark.django_db
def test_task_serializer_valid_data():
    """Test TaskSerializer with valid data."""
    
    user = User.objects.create(username="testuser", email="test@example.com")

    task_data = {
        "title": "Complete Django Project",
        "description": "Finish the Django REST API module",
        "status": "Pending",
        "priority": 2,
        "assigned_to": user.id,
        "due_date": "2025-03-10"
    }

    serializer = TaskSerializer(data=task_data)
    assert serializer.is_valid(), serializer.errors  
    task_instance = serializer.save()
    
    assert task_instance.title == "Complete Django Project"
    assert task_instance.status == "Pending"
    assert task_instance.priority == 2
    assert task_instance.assigned_to == user


@pytest.mark.django_db
def test_task_serializer_invalid_data():
    """Test TaskSerializer with invalid data (missing required fields)."""

    invalid_task_data = {
        "description": "Missing title",
        "status": "Completed",
        "priority": 1
    }

    serializer = TaskSerializer(data=invalid_task_data)
    
    assert not serializer.is_valid()  
    assert "title" in serializer.errors 
    assert "assigned_to" in serializer.errors  


@pytest.mark.django_db
def test_task_serializer_read_only_fields():
    """Test that `created_at` and `updated_at` cannot be modified via the serializer."""

    user = User.objects.create(username="readonlytest", email="readonly@example.com")

    task_data = {
        "title": "Read-Only Test",
        "description": "Checking read-only fields",
        "status": "In Progress",
        "priority": 1,
        "assigned_to": user.id,
        "due_date": "2025-03-10",
        "created_at": datetime(2022, 1, 1),  
        "updated_at": datetime(2022, 1, 1)   
    }

    serializer = TaskSerializer(data=task_data)
    assert serializer.is_valid(), serializer.errors
    task_instance = serializer.save()
    
    assert task_instance.created_at != datetime(2022, 1, 1)  
    assert task_instance.updated_at != datetime(2022, 1, 1)  