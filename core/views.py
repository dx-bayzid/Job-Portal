from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Recruiter, JobSeeker
from jobs.models import Job
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.contrib.auth.decorators import login_required
import re

User = get_user_model()

# Create your views here.
def home(request):
    # Fetch the 6 most recently posted jobs to feature on the homepage
    recent_jobs = Job.objects.all().order_by('-created_at')[:6] 
    
    context = {
        'jobs': recent_jobs
    }
    return render(request, 'accounts/index.html', context)

def register(request):
    if request.method == "POST":
        display_name = request.POST.get('display_name')    
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_password')

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if password != confirm_pass:
            messages.error(request,'Password do not matched')
            return redirect('register')
        if not re.match(pattern, password):
            messages.error(request, "Invalid password. Must contain 8 characters with uppercase, lowercase, number, and special character")
            return redirect('register')
        if User.objects.filter(username = username).exists():
            messages.error(request,'Username already exist!')
            return redirect('register')
        if User.objects.filter(email = email).exists():
            messages.error(request,'Email already exist!')
            return redirect('register')
        
        user = User.objects.create_user(
            full_name = display_name,
            role = user_type,
            username = username,
            email = email,
            profile_pic = profile_pic,
            password = password,
        )
        
        if user_type == 'recruiter':
            Recruiter.objects.create(user = user)

        elif user_type == 'jobseeker':
            JobSeeker.objects.create(user = user)
        
        messages.success(request, 'Registration Successful')
        return redirect('login') 
    
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == "POST":
        user_input = request.POST.get('username_or_email')
        password = request.POST.get('password')
        
        try:
            user_obj = User.objects.get(email = user_input)
            user_name = user_obj.username 
        
        except User.DoesNotExist:
            user_name = user_input 
            
        user = authenticate(request, username = user_name, password = password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid Credential!')
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def logout_view(request):
    
    logout(request)
    messages.success(request, "Logout Successful")
    
    return redirect('login')

@login_required
def profile(request, username):
    # # Security: Ensure users can only edit their own profile
    # if request.user.username != username:
    #     return redirect('profile', username=request.user.username)
    if request.user.role == 'recruiter':
            recruiter = Recruiter.objects.get(user=request.user)
    elif request.user.role == 'jobseeker':
            seeker = JobSeeker.objects.get(user=request.user)

    if request.method == 'POST':
        if request.user.role == 'recruiter':
            company_name = request.POST.get('company_name')
            description = request.POST.get('description')
            company_logo = request.FILES.get('company_logo')

            recruiter.company_name = company_name
            recruiter.description = description
            if company_logo:
                recruiter.company_logo = company_logo
            recruiter.save()
            messages.success(request, "Company profile updated!")

        elif request.user.role == 'jobseeker':
            skill = request.POST.get('skill')
            address = request.POST.get('address')
            bio = request.POST.get('bio')
            cv = request.FILES.get('cv')

            seeker.skill = skill
            seeker.address = address
            seeker.bio = bio
            if cv:
                seeker.cv = cv
            seeker.save()
            messages.success(request, "Professional profile updated!")
            
        return redirect('profile', username=username)


    if request.user.role == 'recruiter':
        context = {
            'user': request.user,
            'recruiter': recruiter
        }
    elif request.user.role == 'jobseeker':
        context = {
            'user': request.user,
            'seeker' : seeker
        }

    return render(request, 'accounts/profile.html', context)

@login_required
def company_profile(request):

    recruiter = Recruiter.objects.get(user=request.user)

    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        description = request.POST.get('description')
        company_logo = request.FILES.get('company_logo')

        recruiter.company_name = company_name
        recruiter.description = description
        
        # Only update the logo if they actually uploaded a new one
        if company_logo:
            recruiter.company_logo = company_logo
            
        # 4. Save to the database
        recruiter.save()
        
        messages.success(request, 'Company profile updated successfully!')
        return redirect('profile', username= request.user.username)

    # If it's a GET request, just pass the recruiter data to pre-fill the form
    context = {
        'recruiter': recruiter
    }
    return render(request, 'accounts/company_profile.html', context)