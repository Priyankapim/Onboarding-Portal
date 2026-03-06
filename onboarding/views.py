from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory, modelformset_factory
from django.db import transaction
from .models import Candidate, Education, WorkExperience, Document
from .forms import CandidateForm, EducationForm, WorkExperienceForm, DocumentForm

def onboarding_form(request, token):
    candidate = get_object_or_404(Candidate, token=token)

    if candidate.is_submitted:
        return render(request, 'onboarding/already_submitted.html', {'candidate': candidate})


    EducationFormSet = inlineformset_factory(
        Candidate,
        Education,
        form=EducationForm,
        extra=0,
        can_delete=True
    )
    edu_formset = EducationFormSet(instance=candidate, prefix='education')

    WorkExperienceFormSet = inlineformset_factory(
        Candidate,
        WorkExperience,
        form=WorkExperienceForm,
        extra=0,
        can_delete=True
    )
    work_formset = WorkExperienceFormSet(instance=candidate, prefix='work')

    DocumentFormSet = modelformset_factory(
        Document,
        form=DocumentForm,
        extra=0,
        can_delete=True
    )
    doc_formset = DocumentFormSet(
        queryset=Document.objects.filter(candidate=candidate),
        prefix='document'
    )

    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        edu_formset = EducationFormSet(request.POST, instance=candidate, prefix='education')
        work_formset = WorkExperienceFormSet(request.POST, instance=candidate, prefix='work')
        doc_formset = DocumentFormSet(request.POST, request.FILES,
                                      queryset=Document.objects.filter(candidate=candidate),
                                      prefix='document')

        if form.is_valid() and edu_formset.is_valid() and work_formset.is_valid() and doc_formset.is_valid():
            with transaction.atomic():
                cand = form.save(commit=False)
                if 'submit' in request.POST:
                    cand.is_submitted = True
                cand.save()

                edu_instances = edu_formset.save(commit=False)
                for obj in edu_formset.deleted_objects:
                    obj.delete()
                for edu in edu_instances:
                    edu.candidate = cand
                    edu.save()

                work_instances = work_formset.save(commit=False)
                for obj in work_formset.deleted_objects:
                    obj.delete()
                for work in work_instances:
                    work.candidate = cand
                    work.save()

                doc_instances = doc_formset.save(commit=False)
                for obj in doc_formset.deleted_objects:
                    obj.delete()
                for doc in doc_instances:
                    doc.candidate = cand
                    doc.save()

            return redirect('onboarding_form', token=candidate.token)
    else:
        form = CandidateForm(instance=candidate)

    return render(request, 'onboarding/form.html', {
        'form': form,
        'edu_formset': edu_formset,
        'work_formset': work_formset,
        'doc_formset': doc_formset,
    })







