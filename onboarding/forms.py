from django import forms
from .models import Candidate, Education, WorkExperience, Document


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'first_name','middle_name','last_name',
            'date_of_birth','place_of_birth',
            'email','contact_number','emergency_contact_number',
            'work_status',

            # 🔥 new fields
            'address_line1', 'address_line2',
            'city', 'state', 'pincode', 'country'
        ]
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}
        labels = {
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
        }

    def __init__(self, *args, **kwargs):
        self.is_submit = kwargs.pop('is_submit', False)
        super().__init__(*args, **kwargs)

        # readonly fields
        readonly_fields = ['first_name', 'last_name', 'email', 'contact_number']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True

        if not self.is_submit:
            # SAVE DRAFT → no required fields
            for field in self.fields.values():
                field.required = False
        else:
            # SUBMIT → required fields
            required_fields = [
                'address',
                'middle_name',
                'date_of_birth',
                'place_of_birth',
                'emergency_contact_number'
            ]
            for field in required_fields:
                self.fields[field].required = True

    def is_valid(self):
        valid = super().is_valid()

        if self.is_submit:  # only on submit
            for field in self.fields:
                if self.errors.get(field):
                    existing_class = self.fields[field].widget.attrs.get('class', '')
                    self.fields[field].widget.attrs['class'] = existing_class + ' error'

        return valid


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['education_type', 'stream', 'percentage', 'grade', 'year_start', 'year_end']
        labels = {
            'year_start': 'Start Year',
            'year_end': 'End Year',
        }

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
        labels = {
            'is_last_company': 'Is this your last company?',
            'date_exit' : 'Exit Date',
            'date_joining' : 'Joining Date',
        }




class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)






