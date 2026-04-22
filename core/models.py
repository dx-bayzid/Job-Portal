from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

    user_type = (
        ('jobseeker', 'Job Seeker'),
        ('recruiter', 'Recruiter')
        # ('value saved in the db', 'show' )
    )
    full_name = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='profile/',null=True,blank=True)
    role = models.CharField(max_length=25,choices=user_type)
    def __str__(self):
        return self.username
    
class JobSeeker(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    skill = models.CharField(max_length=30)
    bio = models.TextField()
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    def __str__(self):
        return f"Seeker {self.user.username}"
    
class Recruiter(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100,blank = True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text="Write a little bit about the company culture and mission.")

    def __str__(self):
        return f"Recruiter {self.user.username}"
    