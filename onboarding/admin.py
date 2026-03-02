from idlelib.configdialog import changes
from tokenize import endpats

from django.contrib import admin
from .models import Candidate, Education, WorkExperience

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'email', 'contact_number', 'is_submitted', 'created_at')



admin.site.register(Education)
admin.site.register(WorkExperience)