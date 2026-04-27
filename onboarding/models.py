from django.contrib.auth.password_validation import password_changed
from django.db import models
from django.core.exceptions import ValidationError
import uuid
import random

class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    # 🔥 NEW ADDRESS FIELDS
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)

    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, default="India", blank=True, null=True)

    contact_number = models.CharField(max_length=15)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    password = models.CharField(max_length=100, blank=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True)
    WORK_STATUS = [
        ('FRESHER', 'Fresher'),
        ('EXPERIENCED', 'Experienced'),
    ]
    work_status = models.CharField(max_length=15, choices=WORK_STATUS, default='FRESHER')
    is_submitted = models.BooleanField(default=False)
    token = models.CharField(max_length=32, default=uuid.uuid4().hex, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    current_step = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Education(models.Model):
    EDUCATION_TYPES = [
        ('SSC', 'SSC'),
        ('HSC', 'HSC'),
        ('BACHELOR', 'Bachelor'),
        ('MASTER', 'Master'),
    ]
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='educations')
    education_type = models.CharField(max_length=20, choices=EDUCATION_TYPES)
    stream = models.CharField(max_length=100, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=20, blank=True)
    year_start = models.IntegerField(null=True, blank=True)
    year_end = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.candidate.first_name} - {self.education_type}"

    class Meta:
        unique_together = ('candidate', 'education_type')


class WorkExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=50, blank=True)
    date_joining = models.DateField(null=True, blank=True)  # <-- make nullable
    date_exit = models.DateField(null=True, blank=True)
    reason_for_job_change = models.CharField(max_length=255, blank=True)
    is_last_company = models.BooleanField(default=False)



    def clean(self):
        if not self.candidate_id:
            return
        if self.candidate.work_status == 'FRESHER' and self.company_name:
            raise ValidationError("Fresher cannot have work experience.")


    def __str__(self):
        return f"{self.company_name} - {self.candidate.first_name}"


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('EDUCATION', 'Education Certificate'),
        ('WORK', 'Work Experience Certificate'),
        ('ID_PROOF', 'ID Proof (Aadhar/PAN/Passport)'),
        ('PHOTO', 'Photo'),
    ]
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.first_name} - {self.document_type}"



def generate_credentials(first_name, last_name):
    num = str(random.randint(10, 99))
    username = f"{first_name.lower()}{last_name[0].upper()}{num}"
    password = f"{first_name.lower()}{last_name.lower()}@{num}"
    return username, password

def generate_credentials(first_name, last_name):
    while True:
        num = str(random.randint(10, 99))
        username = f"{first_name.lower()}{last_name[0].upper()}{num}"


        # check if username already exists
        if not Candidate.objects.filter(username=username).exists():
            break

    password = f"{first_name.lower()}{last_name.lower()}@{num}"
    return username, password











