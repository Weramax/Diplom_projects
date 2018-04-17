import sys

from django.shortcuts import render, redirect
from .models import Project, Species_project, Species_Task
from django.contrib.auth.models import User
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse
from django.views.generic import View


from reportlab.pdfgen import canvas
from reportlab.pdfbase import ttfonts, pdfmetrics

from .utils import render_to_pdf


def generate_pdf(request, pk):

	project = Project.objects.filter(species_id=pk)
	species_projects = Species_project.objects.get(id=pk)

	response = HttpResponse(content_type='application/pdf')

	#response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'


	MyFontObject = ttfonts.TTFont('Arial', sys.path[0] + '/websystem/static/fonts/9041.ttf')
	pdfmetrics.registerFont(MyFontObject)
	p = canvas.Canvas(response)
	p.setLineWidth(.3)
	p.setFont('Arial', 12)
	
	def draw_header(name_project):
		p.setFont('Arial', 18)
		p.drawString(0, 780, name_project.name)
		p.setFont('Arial', 14)
		p.drawString(30, 730, "Название")
		

	def draw_body(x, y, item):
		p.setFont('Arial', 12)
		p.drawString(x, y, item.name + ":")
		p.drawString(x+5, y-10, "Описание")
		p.drawString(x+5, y-20, item.description)
		p.drawString(x+5, y-40, "Исполнитель(и)")
		for itm in item.user.all():
			p.drawString(x+5, y-55, itm.first_name + ' ' + itm.last_name + ";")
			x += 100
		

	
	draw_header(species_projects)
	x = 30
	y = 700
	if len(project) > 0:
		for item in project:
			if y > 30:	
				draw_body(x, y, item)
				y -=100
			else:
				p.showPage()
				y = 700
				draw_header(species_projects)
				draw_body(x, y, item)
				y -=100



		p.showPage()
		p.save()
		context = {'response': response}
		return response
	else:
		return HttpResponse(request.META.get('HTTP_REFERER'))


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
		Project.objects.get_or_create(name = name, species_id=pk,  species_task_id=species_task, user=user_task, finish_task=date_finish, description=description)
		
		

	return render(request, 'projects/create_project_task.html', {'task_species': task_species, 'user_list':user_list})

def delete_project_task(request, pk):

	project = Project.objects.filter(id=pk)
	project.delete()
