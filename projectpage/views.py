from django.shortcuts import render, redirect
from .models import Project, Species_project, Species_Task
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf


class GeneratePDF(View):
	def get(self, request, pk, *args, **kwargs):

		
		template = get_template('invoice.html')
		
		context = {
			"project": Project.objects.filter(species_id=pk),
			"species_project": Species_project.objects.get(id=pk)
         }
		html = template.render(context)
		pdf = render_to_pdf('invoice.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Invoice_%s.pdf" %("12341231")
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")


def main(request):

	species_projects = Species_project.objects.all()

	return render(request, 'projects/index.html', {'species_projects': species_projects , 'mainuser': request.user})

def details(request, pk):
	project = Project.objects.filter(species_id=pk)
		
	species_projects = Species_project.objects.get(id=pk)

	return render(request, 'projects/details_project.html', {'project':project, 'species_projects':species_projects})

def create_project(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		short_description = request.POST.get('short_description')
		description = request.POST.get('description')
		date_finish = request.POST.get('finish_date')
		Species_project.objects.create(name=name, short_description=short_description, description = description, finish_task=date_finish)
		return redirect('/')

	return render(request, 'projects/create_project.html')

def create_project_task(request, pk):
	task_species = Species_Task.objects.all()
	user_list = User.objects.all()

	if request.method == 'POST':
		name = request.POST.get('name')
		description = request.POST.get('description')
		species_task = request.POST.get('species_task')
		date_finish = request.POST.get('finish_date')
		user_task = request.POST.get('user_task')
		Project.objects.get_or_create(name = name, species_id=pk, species_task_id=species_task, user=user_task, finish_task=date_finish, description=description)
		

	return render(request, 'projects/create_project_task.html', {'task_species': task_species, 'user_list':user_list})
