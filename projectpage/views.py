from django.shortcuts import render, redirect

from .models import Project, Species_project, Species_Task


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
		description = request.POST.get('description')
		Species_project.objects.create(name=name, description = description)
		return redirect('/')

	return render(request, 'projects/create_project.html')

def create_project_task(request, pk):
	task_species = Species_Task.objects.all()


	if request.method == 'POST':
		name = request.POST.get('name')
		description = request.POST.get('description')
		species_task = request.POST.get('species_task')

		Project.objects.get_or_create(name = name, species_id=pk, species_task_id=species_task, description=description)
		return redirect('/')

	return render(request, 'projects/create_project_task.html', {'task_species': task_species})
