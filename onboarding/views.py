from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory, modelformset_factory
from django.db import transaction
from .models import Candidate, Education, WorkExperience, Document
from .forms import CandidateForm, EducationForm, WorkExperienceForm, DocumentForm


def onboarding_form(request, token):
    candidate = get_object_or_404(Candidate, token=token)

    if candidate.is_submitted:
        return render(request, 'onboarding/already_submitted.html', {
            'candidate': candidate
        })

    # =========================
    # EDUCATION FORMSET (FIXED)
    # =========================
    EducationFormSet = inlineformset_factory(
        Candidate,
        Education,
        form=EducationForm,
        extra=4,           # Always show 4 forms
        can_delete=False
    )

    # =========================
    # WORK EXPERIENCE FORMSET
    # =========================
    WorkExperienceFormSet = inlineformset_factory(
        Candidate,
        WorkExperience,
        form=WorkExperienceForm,
        extra=3,           # Always show 3 forms
        can_delete=True
    )

    # =========================
    # DOCUMENT FORMSET
    # =========================
    DocumentFormSet = modelformset_factory(
        Document,
        form=DocumentForm,
        extra=4
    )

    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        edu_formset = EducationFormSet(request.POST, instance=candidate)
        work_formset = WorkExperienceFormSet(request.POST, instance=candidate)
        doc_formset = DocumentFormSet(
            request.POST,
            request.FILES,
            queryset=Document.objects.filter(candidate=candidate)
        )

        if form.is_valid() and edu_formset.is_valid() and work_formset.is_valid() and doc_formset.is_valid():

            cand = form.save(commit=False)

            # =========================
            # WORK VALIDATION
            # =========================
            filled_experiences = sum(
                1 for w in work_formset
                if w.cleaned_data.get('company_name')
            )

            if cand.work_status == 'EXPERIENCED' and filled_experiences == 0:
                work_formset.non_form_errors = lambda: [
                    "At least one work experience is required."
                ]
                return render(request, 'onboarding/form.html', locals())

            if cand.work_status == 'FRESHER' and filled_experiences > 0:
                work_formset.non_form_errors = lambda: [
                    "Fresher cannot add work experience."
                ]
                return render(request, 'onboarding/form.html', locals())

            # =========================
            # SAVE ALL
            # =========================
            with transaction.atomic():

                if 'submit' in request.POST:
                    cand.is_submitted = True

                cand.save()

                # ---- Save Education (only filled)
                for edu in edu_formset:
                    if edu.cleaned_data.get('education_type'):
                        e = edu.save(commit=False)
                        e.candidate = cand
                        e.save()

                # ---- Save Work (only filled)
                for work in work_formset:
                    if (
                        work.cleaned_data
                        and not work.cleaned_data.get('DELETE', False)
                        and work.cleaned_data.get('company_name')
                    ):
                        w = work.save(commit=False)
                        w.candidate = cand
                        w.clean()
                        w.save()

                # ---- Save Documents
                for doc in doc_formset:
                    if doc.cleaned_data:
                        d = doc.save(commit=False)
                        d.candidate = cand
                        d.save()

            return redirect('onboarding_form', token=candidate.token)

    else:
        form = CandidateForm(instance=candidate)
        edu_formset = EducationFormSet(instance=candidate)
        work_formset = WorkExperienceFormSet(instance=candidate)
        doc_formset = DocumentFormSet(
            queryset=Document.objects.filter(candidate=candidate)
        )

    return render(request, 'onboarding/form.html', {
        'form': form,
        'edu_formset': edu_formset,
        'work_formset': work_formset,
        'doc_formset': doc_formset,
    })