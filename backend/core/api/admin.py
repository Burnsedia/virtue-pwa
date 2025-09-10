from django.contrib import admin
from .models import Issue, Project, Organization, TimeLog

# Register your models here.
admin.site.register(Issue)
admin.site.register(Project)
admin.site.register(TimeLog)
