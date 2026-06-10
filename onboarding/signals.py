from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Candidate, generate_credentials
from django.core.mail import EmailMultiAlternatives


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
        instance.save(update_fields=['username', 'password'])

        onboarding_link = (
            f"https://hr-onboarding-portal-6y3a.onrender.com/"
            f"onboarding/login/{instance.token}/"
        )

        print("Candidate created. Email sending skipped for testing.")

