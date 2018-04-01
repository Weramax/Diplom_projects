from django.contrib import admin

# Register your models here.
from .models import Project, Species_project, Species_Task


admin.site.register(Project)
admin.site.register(Species_project)
admin.site.register(Species_Task)