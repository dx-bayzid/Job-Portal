from django.contrib import admin
from .models import CustomUser, JobSeeker, Recruiter
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name', 'email', 'role')
    list_filter = ('role', )
    search_fields = ('email', 'username')
    ordering = ('id', )

admin.site.register(Recruiter)
admin.site.register(JobSeeker)
