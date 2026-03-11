from django.db import models
from django.core.exceptions import ValidationError
import uuid

class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    emergency_contact_number = models.CharField(max_length=15, blank=True)
    WORK_STATUS = [
        ('FRESHER', 'Fresher'),
        ('EXPERIENCED', 'Experienced'),
    ]
    work_status = models.CharField(max_length=15, choices=WORK_STATUS, default='FRESHER')
    is_submitted = models.BooleanField(default=False)
    token = models.CharField(max_length=32, default=uuid.uuid4().hex, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
        if self.is_last_company:
            existing_last = WorkExperience.objects.filter(
                candidate=self.candidate, is_last_company=True
            ).exclude(id=self.id)
            if existing_last.exists():
                raise ValidationError("Only one company can be marked as last company.")

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


