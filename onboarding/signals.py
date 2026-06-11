from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Candidate, generate_credentials

import requests


@receiver(post_save, sender=Candidate)
def send_onboarding_email(sender, instance, created, **kwargs):

    if not created:
        return

    username, password = generate_credentials(
        instance.first_name,
        instance.last_name
    )

    instance.username = username
    instance.password = password
    instance.save(update_fields=["username", "password"])

    onboarding_link = (
        f"https://hr-onboarding-portal-6y3a.onrender.com/"
        f"onboarding/login/{instance.token}/"
    )

    html_content = f"""
    <html>
    <body>

    <p>Hi {instance.first_name},</p>

    <p>Welcome to <b>NabiTech Solution</b>.</p>

    <p>Please complete your onboarding using the link below:</p>

    <p>
        <a href="{onboarding_link}">
            {onboarding_link}
        </a>
    </p>

    <p>
        <b>Login Details</b><br><br>

        Username: {username}<br>
        Password: {password}
    </p>

    <p>
        Please change your password after your first login.
    </p>

    <br>

    <p>
        Regards,<br>
        HR Team
    </p>

    </body>
    </html>
    """

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": "NabiTech HR",
            "email": settings.DEFAULT_FROM_EMAIL,
        },
        "to": [
            {
                "email": instance.email,
            }
        ],
        "subject": "Welcome to NabiTech – Complete Your Onboarding",
        "htmlContent": html_content,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=20,
    )

    print(response.status_code)
    print(response.text)