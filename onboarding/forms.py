from django import forms
from .models import Candidate, Education, WorkExperience, Document

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'first_name', 'middle_name', 'last_name',
            'date_of_birth', 'place_of_birth',
            'email', 'contact_number', 'emergency_contact_number',
            'work_status'
        ]
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        readonly_fields = ['first_name','middle_name','last_name','email','contact_number']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['education_type', 'stream', 'percentage', 'grade', 'year_start', 'year_end']
        #YEARS = [(y, y) for y in range(1980, 2031)]

        #widgets = {
        #    'year_start': forms.Select(choices=YEARS),
         #   'year_end': forms.Select(choices=YEARS),
        #}


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'designation', 'date_joining', 'date_exit', 'reason_for_job_change', 'is_last_company']
        widgets = {
            'date_joining': forms.DateInput(attrs={'type': 'date'}),
            'date_exit': forms.DateInput(attrs={'type': 'date'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']

