from django.db import models
from django.contrib.auth.models import User

 

class Task(models.Model):
    """Represents a task in the task manager."""

    STATUS_CHOICES = [
        ('Pending', 'Pending'), 
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    PRIORITIES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )

    title = models.CharField(max_length=255, verbose_name="Task Title", db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name="Task Description")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending", verbose_name="Task Status", db_index=True)
    priority = models.IntegerField(default=1, choices=PRIORITIES, verbose_name="Task Priority", db_index=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks", verbose_name="Task Assigned To", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    due_date = models.DateField(blank=True, null=True, verbose_name="Due Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completed At")
    observation = models.TextField(blank=True, null=True, verbose_name="Observations")


    class Meta:
        ordering = ["priority", "due_date"]

    def __str__(self):
        return f"{self.title} - {self.status} (Priority: {self.priority})"


