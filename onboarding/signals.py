from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Candidate, generate_credentials

import requests


@receiver(post_save, sender=Candidate)
def send_onboarding_email(sender, instance, created, **kwargs):

    if not created:
        return

    # Generate username and password
    username, password = generate_credentials(
        instance.first_name,
        instance.last_name
    )

    # Save credentials
    instance.username = username
    instance.password = password
    instance.save(update_fields=["username", "password"])

    # Onboarding URL
    onboarding_link = (
        f"https://hr-onboarding-portal-6y3a.onrender.com/"
        f"onboarding/login/{instance.token}/"
    )

    # HTML Email
    html_content = f"""
    <html>
    <body style="font-family: Arial, Helvetica, sans-serif; font-size:15px; color:#333333; line-height:1.7;">

        <p>Hi {instance.first_name},</p>

        <p>
            Welcome to <strong>NabiTech Solution</strong> 👋
        </p>

        <p>
            Please complete your onboarding using the link below:
        </p>

        <p>
            <a href="{onboarding_link}">
                {onboarding_link}
            </a>
        </p>

        <p>
            <strong>Login Details:</strong><br><br>

            User ID: {username}<br>
            Password: {password}
        </p>

        <p>
            For security reasons, please change your password after your first login.
        </p>

        <p>
            If you need any assistance, feel free to reach out.
        </p>

        <br>

        <p>
            Thanks &amp; Regards,<br>
            <strong>HR Team</strong><br>
            NabiTech Solution
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

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=20,
        )

        print("Brevo Status:", response.status_code)
        print("Brevo Response:", response.text)

    except Exception as e:
        print("Email sending failed:", str(e))

