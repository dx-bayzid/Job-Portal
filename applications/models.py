from django.db import models
from core.models import JobSeeker
from jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents a job seeker from applying to the same job twice
        unique_together = ('job', 'applicant') 

    def __str__(self):
        return f"{self.applicant.user.username} applied for {self.job.title}"