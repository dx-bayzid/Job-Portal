from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from .models import Application

@login_required
def apply_job(request, job_id):
    if request.method == 'POST':
        if request.user.role != 'jobseeker':
            messages.error(request, "Only job seekers can apply for jobs.")
            return redirect('job_details', job_id=job_id)

        job = get_object_or_404(Job, id=job_id)
        seeker = request.user.jobseeker

        # NEW: Check if the user has uploaded a CV
        if not seeker.cv:
            messages.error(request, "You must upload a CV to your profile before applying for jobs.")
            # Redirect them to their profile so they can upload it
            return redirect('profile', username=request.user.username)

        # Check if already applied
        if Application.objects.filter(job=job, applicant=seeker).exists():
            messages.warning(request, "You have already applied for this job.")
        else:
            Application.objects.create(job=job, applicant=seeker)
            messages.success(request, "Application submitted successfully!")

        return redirect('job_details', job_id=job_id)