from django.db import models
from core.models import Recruiter

# Create your models here.
class Job(models.Model):
    
    TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('remote', 'Remote'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )
    
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    title  = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    description = models.TextField()
    openings = models.IntegerField()
    salary = models.IntegerField()
    job_type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    location = models.CharField(max_length=50)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title 