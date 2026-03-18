from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory, modelformset_factory
from django.db import transaction

from .models import Candidate, Education, WorkExperience, Document
from .forms import CandidateForm, EducationForm, WorkExperienceForm, DocumentForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Candidate

def login_view(request, token):
    candidate = get_object_or_404(Candidate, token=token)

    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == candidate.username and password == candidate.password:
            request.session['candidate_id'] = candidate.id
            return redirect('onboarding_form', token=token)
        else:
            error = "Invalid User ID or Password"

    return render(request, 'onboarding/login.html', {
        'candidate': candidate,
        'error': error
    })


def onboarding_form(request, token):

    candidate = get_object_or_404(Candidate, token=token)


    # check login
    if request.session.get('candidate_id') != candidate.id:
        return redirect('login_view', token=token)

    if candidate.is_submitted:
        return render(request, 'onboarding/already_submitted.html', {'candidate': candidate})


    EducationFormSet = inlineformset_factory(
        Candidate,
        Education,
        form=EducationForm,
        extra=0,
        can_delete=True
    )

    WorkExperienceFormSet = inlineformset_factory(
        Candidate,
        WorkExperience,
        form=WorkExperienceForm,
        extra=0,
        can_delete=True
    )

    DocumentFormSet = modelformset_factory(
        Document,
        form=DocumentForm,
        extra=0,
        can_delete=True
    )


    if request.method == 'POST':

        form = CandidateForm(request.POST, instance=candidate)

        edu_formset = EducationFormSet(
            request.POST,
            instance=candidate,
            prefix='education'
        )

        work_formset = WorkExperienceFormSet(
            request.POST,
            instance=candidate,
            prefix='work'
        )


        doc_formset = DocumentFormSet(
            request.POST,
            request.FILES,
            queryset=Document.objects.filter(candidate=candidate),
            prefix='document'
        )


        if form.is_valid() and edu_formset.is_valid() and work_formset.is_valid() and doc_formset.is_valid():


            education_types = []

            for edu in edu_formset.cleaned_data:
                if edu and not edu.get('DELETE', False):
                    education_types.append(edu.get('education_type'))

            missing_education = []

            if 'SSC' not in education_types:
                missing_education.append("SSC")

            if 'HSC' not in education_types:
                missing_education.append("HSC")

            if 'BACHELOR' not in education_types:
                missing_education.append("Bachelor")

            if missing_education:
                edu_formset._non_form_errors = edu_formset.error_class([
                    f"Please add education details for: {', '.join(missing_education)}"
                ])



                return render(request, 'onboarding/form.html', {
                    'form': form,
                    'edu_formset': edu_formset,
                    'work_formset': work_formset,
                    'doc_formset': DocumentFormSet(request.POST, request.FILES,
                                                   queryset=Document.objects.filter(candidate=candidate),
                                                   prefix='document')
                })


            doc_types = []

            for doc in doc_formset.cleaned_data:
                if doc and not doc.get('DELETE', False):
                    doc_types.append(doc.get('document_type'))

            missing_docs = []

            if 'EDUCATION' not in doc_types:
                missing_docs.append("Education Certificate")

            if 'ID_PROOF' not in doc_types:
                missing_docs.append("ID Proof")

            if 'PHOTO' not in doc_types:
                missing_docs.append("Photo")

            if missing_docs:
                doc_formset._non_form_errors = doc_formset.error_class([
                    f"Please upload required documents: {', '.join(missing_docs)}"
                ])

                return render(request, 'onboarding/form.html', {
                    'form': form,
                    'edu_formset': edu_formset,
                    'work_formset': work_formset,
                    'doc_formset': doc_formset,
                })


            if form.cleaned_data.get('work_status') == 'EXPERIENCED':

                has_experience = False

                for work in work_formset.cleaned_data:
                    if work and not work.get('DELETE', False):
                        has_experience = True

                if not has_experience:
                    work_formset._non_form_errors = work_formset.error_class([
                        "Please add your work experience details."
                    ])

                    return render(request, 'onboarding/form.html', {
                        'form': form,
                        'edu_formset': edu_formset,
                        'work_formset': work_formset,
                        'doc_formset': doc_formset,
                    })


                if 'WORK' not in doc_types:
                    doc_formset._non_form_errors = doc_formset.error_class([
                        "Please upload work experience certificate."
                    ])

                    return render(request, 'onboarding/form.html', {
                        'form': form,
                        'edu_formset': edu_formset,
                        'work_formset': work_formset,
                        'doc_formset': doc_formset,
                    })



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

        edu_formset = EducationFormSet(
            instance=candidate,
            prefix='education'
        )

        work_formset = WorkExperienceFormSet(
            instance=candidate,
            prefix='work'
        )

        doc_formset = DocumentFormSet(
            queryset=Document.objects.filter(candidate=candidate),
            prefix='document'
        )


    return render(request, 'onboarding/form.html', {
        'form': form,
        'edu_formset': edu_formset,
        'work_formset': work_formset,
        'doc_formset': doc_formset,
    })

