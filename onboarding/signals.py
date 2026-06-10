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

        from django.core.mail import EmailMultiAlternatives

        email = EmailMultiAlternatives(
            subject="Welcome to NabiTech – Complete Your Onboarding",
            body="Please view this email in HTML format.",
            from_email=settings.EMAIL_HOST_USER,
            to=[instance.email],
        )

        html_content = f"""
<div style="font-family: Arial, sans-serif; font-size:14px; color:#1e293b; line-height:1.6;">

<p>Hi {instance.first_name},</p>

<p>Welcome to <b>NabiTech Solution</b> 👋</p>

<p>Please complete your onboarding using the link below:</p>

<p>
<a href="{onboarding_link}" style="color:#6366f1; text-decoration:none;">
{onboarding_link}
</a>
</p>

<p><b>Login Details:</b><br>
User ID: {username}<br>
Password: {password}
</p>

<p style="color:#6b7280;">
For security reasons, please change your password after your first login.
</p>

<p>If you need any assistance, feel free to reach out.</p>

<p>
Thanks & Regards,<br>
HR Team<br>
NabiTech Solution
</p>

</div>
"""

        email.attach_alternative(html_content, "text/html")

        try:
            email.send(fail_silently=False)
            print("Email sent successfully")
        except Exception as e:
            print("Email sending failed:", repr(e))


