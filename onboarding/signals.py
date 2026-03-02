from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Candidate


@receiver(post_save, sender=Candidate)
def send_onboarding_email(sender, instance, created, **kwargs):
    if created:
        onboarding_link = f"http://127.0.0.1:8000/onboarding/form/{instance.token}/"

        send_mail(
            subject="Complete Your Onboarding",
            message=f"""
Hello {instance.first_name},

Please complete your onboarding form using the link below:

{onboarding_link}

Thank you.
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )