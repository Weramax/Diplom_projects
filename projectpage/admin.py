from django.contrib import admin

# Register your models here.
from .models import Project, Species_project, Species_Task, UserProject, Documents


admin.site.register(Project)
admin.site.register(Species_project)
admin.site.register(Species_Task)
admin.site.register(UserProject)
admin.site.register(Documents)