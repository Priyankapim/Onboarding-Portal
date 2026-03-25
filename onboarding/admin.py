
#Admin
#Admin@123
from django.contrib import admin
from .models import Candidate, Education, WorkExperience, Document

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'email', 'username', 'contact_number', 'address', 'is_submitted', 'created_at')


admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Document)
