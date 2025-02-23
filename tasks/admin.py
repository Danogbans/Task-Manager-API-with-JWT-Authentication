from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "assigned_to", "due_date", "created_at")
    list_filter = ("status", "priority", "due_date")
    search_fields = ("title", "description", "assigned_to__username")
    ordering = ("priority", "due_date")
    date_hierarchy = "created_at"  
    list_editable = ("status", "priority", "due_date")
