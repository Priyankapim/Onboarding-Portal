from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Candidate, generate_credentials


@receiver(post_save, sender=Candidate)
def send_onboarding_email(sender, instance, created, **kwargs):
    if created:


        username, password = generate_credentials(
            instance.first_name,
            instance.last_name
        )

        # save in DB
        instance.username = username
        instance.password = password
        instance.save()


        onboarding_link = f"http://127.0.0.1:8000/onboarding/login/{instance.token}/"

        send_mail(
            subject="Complete Your Onboarding",
            message=f"""
Hello {instance.first_name},

Your login credentials:

User ID: {username}
Password: {password}

Click below to login:
{onboarding_link}

Thank you.
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )
