from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from applications.models import Application
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Create your views here.

@login_required
def post_job(request):
    if request.method == "POST":
        job_title = request.POST.get('title')
        company_name = request.POST.get('company')
        job_type = request.POST.get('job_type')
        job_location = request.POST.get('location')
        salary = request.POST.get('salary')
        vacancy = request.POST.get('openings')
        application_deadline = request.POST.get('deadline')
        job_description = request.POST.get('description')
        
        recruiter_profile = request.user.recruiter
        
        Job.objects.create(
            recruiter = recruiter_profile,
            title = job_title,
            company = company_name,
            description = job_description,
            openings = vacancy,
            salary = salary,
            job_type = job_type,
            location = job_location,
            deadline = application_deadline
        )
        messages.success(request, 'Job Created Successfully!')
        return redirect('profile',username= request.user.username)        
        
    return render(request, 'jobs/post_job.html')

def job_list(request):
   
    jobs = Job.objects.all()

    query = request.GET.get('q')
    
    if query:
        jobs = Job.objects.filter(
            Q(title__icontains = query) |
            Q(company__icontains = query) |
            Q(job_type__icontains = query) |
            Q(location__icontains= query)
        )

    sort = request.GET.get('sort')
    
    if sort == 'newest':
        jobs = jobs.order_by('-created_at')
    elif sort == 'oldest':
        jobs = jobs.order_by('created_at')
    else:
        jobs = jobs.order_by('-created_at')
   
    context = {
        'jobs': jobs,
        'query' : query
    }
    
    return render(request, 'jobs/job_list.html', context)

def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    
    if request.user.is_authenticated and request.user.role == 'jobseeker':
        has_applied = Application.objects.filter(job=job, applicant=request.user.jobseeker).exists()
    
    context = {
        'job': job,
        'today': timezone.now().date(), # Used to check the deadline
        'has_applied': has_applied      # Used to swap the Apply button
    }
    
    return render(request, 'jobs/job_details.html', context)