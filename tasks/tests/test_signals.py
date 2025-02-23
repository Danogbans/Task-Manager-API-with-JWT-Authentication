import pytest
from django.utils.timezone import now
from django.core.mail import send_mail
from django.core import mail
from unittest.mock import patch
from django.contrib.auth.models import User
from tasks.models import Task
from django.conf import settings




@pytest.mark.django_db
def test_auto_set_completed_at():
    """Test that 'completed_at' is automatically set when a task's status is 'Completed'."""
    user = User.objects.create(username="testuser", email="testuser@example.com")
    task = Task.objects.create(title="Test Task", status="Pending", assigned_to=user)

    # Task initially has no completed_at
    assert task.completed_at is None

    # Update status to 'Completed'
    task.status = "Completed"
    task.save()

    # Refresh task from the database
    task.refresh_from_db()

    # Ensure 'completed_at' is set after saving
    assert task.completed_at is not None


@pytest.mark.django_db
@patch("tasks.signals.send_mail")
def test_send_task_assignment_email(mock_send_mail):
    """Test that an email is sent when a task is assigned to a user."""
    user = User.objects.create(username="testuser", email="testuser@example.com")

    # Create a new task (should trigger post_save)
    task = Task.objects.create(title="Test Task", assigned_to=user)

    # Ensure send_mail was called once
    mock_send_mail.assert_called_once_with(
        "New Task Assigned",
        f"Hello {user.username},\n\nYou have been assigned a new task: {task.title}.",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

   