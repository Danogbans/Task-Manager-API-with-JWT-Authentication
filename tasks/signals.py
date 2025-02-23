import logging
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Task



logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Task)
def auto_set_completed_at(sender, instance, **kwargs):
    if instance.status == "Completed" and instance.completed_at is None:
        instance.completed_at = now()


@receiver(post_save, sender=Task)
def send_task_assignment_email(sender, instance, created, **kwargs):
    #Send an email to the assigned user when a new task is created.
    if created and instance.assigned_to and instance.assigned_to.email:
        try:
            send_mail(
                "New Task Assigned",
                f"Hello {instance.assigned_to.username},\n\nYou have been assigned a new task: {instance.title}.",
                settings.EMAIL_HOST_USER,  # Uses the configured sender email
                [instance.assigned_to.email], 
                fail_silently=False  # Prevents errors from breaking the app
            )
            logger.info(f"Email sent successfully to {instance.assigned_to.email}")
        except Exception as e:
            logger.error(f"Error sending email to {instance.assigned_to.email}: {e}")  # Logs error in case of failure



