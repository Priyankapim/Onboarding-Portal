from django.forms import inlineformset_factory, modelformset_factory
from django.db import transaction
from .models import Candidate, Education, WorkExperience, Document
from .forms import CandidateForm, EducationForm, WorkExperienceForm, DocumentForm, ChangePasswordForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def login_view(request, token):
    candidate = get_object_or_404(Candidate, token=token)
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == candidate.username and password == candidate.password:
            request.session['candidate_id'] = candidate.id
            return redirect('personal_view', token=token)
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

        is_submit = 'submit' in request.POST

        form = CandidateForm(request.POST, instance=candidate, is_submit=is_submit)

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

        if not is_submit:

            form.save()
            edu_formset.save()
            work_formset.save()
            doc_formset.save()

            messages.success(request, "Draft saved successfully")
            return redirect('onboarding_form', token=candidate.token)


        else:

            if form.is_valid() and edu_formset.is_valid() and work_formset.is_valid() and doc_formset.is_valid():

                #education validation
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
                        'doc_formset': doc_formset,
                        'candidate': candidate
                    })

                #document validation
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
                        'candidate': candidate
                    })

                #work validation
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
                            'candidate': candidate
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
                            'candidate': candidate
                        })

                #save all
                with transaction.atomic():

                    cand = form.save(commit=False)
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

                messages.success(request, "Form submitted successfully")
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
        'candidate': candidate
    })

def logout_view(request, token):
    request.session.flush()
    return redirect('login_view', token=token)


def change_password(request, token):

    candidate = get_object_or_404(Candidate, token=token)

    if request.session.get('candidate_id') != candidate.id:
        return redirect('login_view', token=token)

    form = ChangePasswordForm()

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            old = form.cleaned_data['old_password']
            new = form.cleaned_data['new_password']
            confirm = form.cleaned_data['confirm_password']

            if old != candidate.password:
                form.add_error('old_password', "Wrong old password")

            elif new != confirm:
                form.add_error('confirm_password', "Passwords do not match")

            else:
                candidate.password = new
                candidate.save()
                messages.success(request, "Password updated successfully")
                return redirect('onboarding_form', token=token)

    return render(request, 'onboarding/change_password.html', {
        'form': form,
        'token': token,
        'candidate': candidate
    })

def personal_view(request, token):
    candidate = get_object_or_404(Candidate, token=token)

    if request.session.get('candidate_id') != candidate.id:
        return redirect('login_view', token=token)

    form = CandidateForm(request.POST or None, instance=candidate)

    if request.method == "POST":

        if form.is_valid():
            form.save()

            if "next" in request.POST:
                candidate.current_step = 2
                candidate.save()
                return redirect('education_view', token=token)

    return render(request, 'onboarding/personal.html', {
        'form': form,
        'candidate': candidate,
        'step': candidate.current_step
    })

def education_view(request, token):
    candidate = get_object_or_404(Candidate, token=token)

    if request.session.get('candidate_id') != candidate.id:
        return redirect('login_view', token=token)

    if candidate.current_step < 2:
        return redirect('personal_view', token=token)

    EducationFormSet = inlineformset_factory(
        Candidate, Education, form=EducationForm, extra=0, can_delete=True
    )

    formset = EducationFormSet(request.POST or None, instance=candidate)

    if request.method == "POST":

        if "prev" in request.POST:
            candidate.current_step = 1
            candidate.save()
            return redirect('personal_view', token=token)

        if formset.is_valid():
            formset.save()

            if "next" in request.POST:
                candidate.current_step = 3
                candidate.save()
                return redirect('work_view', token=token)

    return render(request, 'onboarding/education.html', {
        'formset': formset,
        'candidate': candidate,
        'step': candidate.current_step
    })

def work_view(request, token):
    candidate = get_object_or_404(Candidate, token=token)

    if request.session.get('candidate_id') != candidate.id:
        return redirect('login_view', token=token)

    if candidate.current_step < 3:
        return redirect('education_view', token=token)

    WorkFormSet = inlineformset_factory(
        Candidate, WorkExperience, form=WorkExperienceForm, extra=0, can_delete=True
    )

    formset = WorkFormSet(
        request.POST or None,
        instance=candidate,
        prefix='workexperience_set'
    )

    if request.method == "POST":

        if "prev" in request.POST:
            candidate.current_step = 2
            candidate.save()
            return redirect('education_view', token=token)

        if formset.is_valid():
            formset.save()

            if "next" in request.POST:
                candidate.current_step = 4
                candidate.save()
                return redirect('document_view', token=token)

        else:
            print("FORMSET ERRORS:", formset.errors)
            print("NON FORM ERRORS:", formset.non_form_errors())

            if "next" in request.POST:
                candidate.current_step = 4
                candidate.save()
                return redirect('document_view', token=token)


    return render(request, 'onboarding/work.html', {
        'formset': formset,
        'candidate': candidate,
        'step': candidate.current_step
    })

def document_view(request, token):
    candidate = get_object_or_404(Candidate, token=token)

    if request.session.get('candidate_id') != candidate.id:
        return redirect('login_view', token=token)

    if candidate.current_step < 4:
        return redirect('work_view', token=token)

    DocumentFormSet = modelformset_factory(
        Document, form=DocumentForm, extra=0, can_delete=True
    )

    formset = DocumentFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=Document.objects.filter(candidate=candidate)
    )

    if request.method == "POST":

        if "prev" in request.POST:
            candidate.current_step = 3
            candidate.save()
            return redirect('work_view', token=token)

        if formset.is_valid():

            # SAVE FIRST
            instances = formset.save(commit=False)

            for obj in formset.deleted_objects:
                obj.delete()

            for doc in instances:
                doc.candidate = candidate
                doc.save()


            # EDUCATION
            educations = Education.objects.filter(candidate=candidate)
            edu_types = [e.education_type for e in educations]

            missing_edu = []
            if 'SSC' not in edu_types:
                missing_edu.append("SSC")
            if 'HSC' not in edu_types:
                missing_edu.append("HSC")
            if 'BACHELOR' not in edu_types:
                missing_edu.append("Bachelor")

            if missing_edu:
                messages.error(request, f"Missing education: {', '.join(missing_edu)}")
                return redirect('education_view', token=token)

            # DOCUMENT
            docs = Document.objects.filter(candidate=candidate)
            doc_types = [d.document_type for d in docs]

            missing_docs = []
            if 'EDUCATION' not in doc_types:
                missing_docs.append("Education Certificate")
            if 'ID_PROOF' not in doc_types:
                missing_docs.append("ID Proof")
            if 'PHOTO' not in doc_types:
                missing_docs.append("Photo")

            if missing_docs:
                messages.error(request, f"Missing documents: {', '.join(missing_docs)}")
                return redirect('document_view', token=token)

            # WORK
            if candidate.work_status == 'EXPERIENCED':
                works = WorkExperience.objects.filter(candidate=candidate)

                if not works.exists():
                    messages.error(request, "Please add work experience")
                    return redirect('work_view', token=token)

                if 'WORK' not in doc_types:
                    messages.error(request, "Upload work certificate")
                    return redirect('document_view', token=token)

            # FINAL SUBMIT
            candidate.is_submitted = True
            candidate.save()

            messages.success(request, "Form submitted successfully")
            return render(request, 'onboarding/already_submitted.html')

    return render(request, 'onboarding/documents.html', {
        'formset': formset,
        'candidate': candidate,
        'step': candidate.current_step
    })
