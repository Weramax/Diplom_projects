import sys

from django.shortcuts import render, redirect
from .models import Project, Species_project, Species_Task, UserProject, Documents

from django.conf import settings


from django.contrib.auth.models import User
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse
from django.views.generic import View


from reportlab.pdfgen import canvas
from reportlab.pdfbase import ttfonts, pdfmetrics

from django.views.generic.edit import FormView
from .forms import UploadFileForm





def check_auth(request):
	if not request.user.is_authenticated():
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))



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
	if not request.user.is_authenticated:
		return redirect('auth/login')
	else:
		species_projects = Species_project.objects.all()
		return render(request, 'projects/index.html', {'species_projects': species_projects , 'mainuser': request.user})

def details(request, pk):
	if not request.user.is_authenticated:
		return redirect('auth/login')
	else:
		project = Project.objects.filter(species_id=pk)	
		species_projects = Species_project.objects.get(id=pk)
		documents = Documents.objects.filter(species_id = pk)
		if request.method == 'POST':
			form = UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				instance = Documents(species_id = pk, name=request.POST.get('name'), file = request.FILES['file'])
				instance.save()
				return redirect('/project/'+pk)
		else:
			form = UploadFileForm()


		return render(request, 'projects/details_project.html', {'form': form, 'project':project, 'species_projects':species_projects, 'documents':documents})

def details_user(request):
	if not request.user.is_authenticated:
		return redirect('auth/login')
	else:
		project = Project.objects.filter(user = request.user.pk)
		return render(request, 'projects/my_details.html', {'project':project})

def create_project(request):
	if not request.user.is_authenticated:
		return redirect('auth/login/')
	else:
		if request.method == 'POST':
			name = request.POST.get('name')
			short_description = request.POST.get('short_description')
			description = request.POST.get('description')
			date_finish = request.POST.get('finish_date')
			Species_project.objects.create(name=name, short_description=short_description, description = description, finish_task=date_finish)
			return redirect('/')

		return render(request, 'projects/create_project.html')

def create_project_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    else:
        task_species = Species_Task.objects.all()
        user_list = User.objects.all()

        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            species_task = request.POST.get('species_task')
            date_finish = request.POST.get('finish_date')
            user_task = request.POST.getlist('user_task')
            project_task = Project.objects.get_or_create(name = name, species_id=pk,  species_task_id=species_task, finish_task=date_finish, description=description)

            for itm in user_task:
                UserProject.objects.get_or_create(project = project_task[0], user_id = int(itm))

            return redirect('/project/'+pk)


        return render(request, 'projects/create_project_task.html', {'task_species': task_species, 'user_list':user_list})


def update_project_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    else:
        user_list = User.objects.all()
        task_species = Species_Task.objects.all()
        project_select = Project.objects.get(id = pk)

        if request.method == 'POST':
            project_select.delete()
            species_project_id = request.POST.get('species_project_id')
            name = request.POST.get('name')
            description = request.POST.get('description')
            species_task = request.POST.get('species_task')
            date_finish = request.POST.get('finish_date')
            user_task = request.POST.getlist('user_task')
            project_task = Project.objects.get_or_create(name = name, species_id=species_project_id,  species_task_id=species_task, finish_task=date_finish, description=description)

            for itm in user_task:
                user_main = UserProject.objects.get_or_create(project = project_task[0], user_id = int(itm))

            return redirect('/project/'+species_project_id)



        return render(request, 'projects/update_project_task.html', {'task_species': task_species, 'user_list': user_list, 'project_select': project_select})



def delete_project_task(request, pk):

    if not request.user.is_authenticated:
        return redirect('auth/login')
    else:
        project = Project.objects.filter(id=pk)
        project.delete()
        return redirect('/')

def complete_task(request, pk):
	if not request.user.is_authenticated:
		return redirect('auth/login')
	else:
		project = Project(id = pk)
		project._do_update(complete_value = '1')
		return redirect('/')