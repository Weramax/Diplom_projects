import sys
import datetime
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Project, Species_project, Species_Task, UserProject, Documents, Comment

from django.conf import settings


from django.contrib.auth.models import User
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse
from django.views.generic import View



from reportlab.pdfgen import canvas
from reportlab.pdfbase import ttfonts, pdfmetrics

from django.views.generic.edit import FormView
from .forms import UploadFileForm, CommentForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf



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
		p.drawString(60, 780, name_project.name)
		p.setFont('Arial', 14)
		p.line(350,778,580,778)
		p.setFont('Arial', 12)
		p.drawString(350, 765, 'Проект завершен на '+ str(name_project.progress_value) + '%')
		p.line(350,763,500,763)
		p.drawString(350, 780, 'Дата завершения проекта:')
		date = datetime.datetime.strftime(name_project.finish_task, '%Y-%m-%d')
		p.setFont('Arial', 14)
		p.drawString(505, 780, date)
		p.drawString(390, 740, 'Подпись')
		p.line(450, 740, 580, 740)
		p.drawString(30, 715, 'Описание проекта:')
		p.drawString(30, 699,  name_project.description)

	def draw_body(x, y, item):
		p.setFont('Arial', 12)
		p.drawString(x, y, "Задача" + "  "+item.name + ":")
		p.drawString(x+5, y-20, "Описание")
		p.drawString(x+5, y-35, item.description)
		p.drawString(x+5, y-55, "Исполнитель(и)")
		z = x

		for itm in item.user.all():
			p.drawString(z+5, y-65, itm.first_name + ' ' + itm.last_name + ";")
			z += 100
		p.drawString(x + 5, y - 85, 'Прогресс задачи:')
		for items in item.complete_value:
			if items != " ":
				p.drawString(x + 130, y - 85, 'Выполнено')
			else:
				p.drawString(x +130, y -85, 'Не выполнено')
		p.line(x, y, x+250, y)

	
	draw_header(species_projects)
	x = 30
	y = 650
	if len(project) > 0:
		for item in project:
			if y > 50:
				draw_body(x, y, item)
				y -=120
			else:
				p.showPage()
				y = 700
				draw_header(species_projects)
				draw_body(x, y, item)
				y -=120



		p.showPage()
		p.save()
		context = {'response': response}
		return response
	else:
		return HttpResponse(request.META.get('HTTP_REFERER'))

def generate_pdf_users(request, pk):
	project = Project.objects.filter(user=pk)
	user = User.objects.filter(id = pk)

	response = HttpResponse(content_type='application/pdf')

	# response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'


	MyFontObject = ttfonts.TTFont('Arial', sys.path[0] + '/websystem/static/fonts/9041.ttf')
	pdfmetrics.registerFont(MyFontObject)
	p = canvas.Canvas(response)
	p.setLineWidth(.3)
	p.setFont('Arial', 12)

	def draw_header(user):
		p.setFont('Arial', 18)
		for itm in user.all():
			p.drawString(60, 780, itm.first_name + "  "+ itm.last_name)

	def draw_body(x, y, item):
		p.setFont('Arial', 12)
		p.drawString(x, y, "Задача" + "  "+item.name + ":" + " В проекте" + str(item.species))
		p.drawString(x+5, y-20, "Описание")
		p.drawString(x+5, y-35, item.description)
		p.drawString(x+5, y-55, "Исполнитель(и)")
		z = x

		for itm in item.user.all():
			p.drawString(z+5, y-65, itm.first_name + ' ' + itm.last_name + ";")
			z += 100
		p.drawString(x + 5, y - 85, 'Прогресс задачи:')
		for items in item.complete_value:
			if items != " ":
				p.drawString(x + 130, y - 85, 'Выполнено')
			else:
				p.drawString(x +130, y -85, 'Не выполнено')
		p.line(x, y, x+250, y)

	draw_header(user)
	x = 30
	y = 700
	if len(project) > 0:
		for item in project:
			if y > 50:
				draw_body(x, y, item)
				y -= 120
			else:
				p.showPage()
				y = 700
				draw_header(user)
				draw_body(x, y, item)
				y -= 120

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
		user_all = User.objects.all()
		for project_id in species_projects:
			project = Project.objects.filter(species = project_id)
			print (len(project))
			if len(project) > 0:
				len_complete = (itm for itm in project if itm.complete_value == "1")
				progress_bar = (((len(list(len_complete))) * 100 ) // len(project))
				project_id.progress_value = progress_bar
				project_id.save()

		return render(request, 'projects/index.html', {'species_projects': species_projects , 'mainuser': request.user, 'user_all':user_all})

def details(request, pk):
	if not request.user.is_authenticated:
		return redirect('auth/login')
	else:
		sort = request.GET.getlist('sort')
		project = Project.objects.filter(species_id=pk).order_by(*sort)
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


		return render(request, 'projects/details_project.html', {'form': form, 'project':project, 'species_projects':species_projects, 'documents':documents, 'date_now':datetime.datetime.now().strftime("%Y-%b-%d")})

def details_user(request):
	if not request.user.is_authenticated:
		return redirect('auth/login')
	else:
		project = Project.objects.filter(user = request.user.pk)
		return render(request, 'projects/my_details.html', {'project':project})

def details_task_project(request, pk):
	if not request.user.is_authenticated:
		return redirect('auth/login')
	else:

		project = Project.objects.filter(id = pk)
		comments = Comment.objects.filter(project_id = pk)
		if request.method == "POST":
			text = request.POST.get('comment_text')
			comments = Comment.objects.get_or_create(project_id_id = pk, author_id = request.user, content = text)
			return redirect('/project/task-details/'+pk)




		for itm in project:
			print (itm.species_task)
			if (datetime.date.today() - itm.finish_task).days >=  0 and itm.complete_value == '1':
				if itm.species_task_id == 2:
					date_now =  datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days = 7), '%Y-%m-%d')
					itm.finish_task = date_now
					itm.complete_value = 0
					itm.save()

		return render(request, 'projects/task_details_project.html', {'project':project, 'comments':comments})

def create_project(request):
	if not request.user.is_authenticated:
		return redirect('auth/login/')
	else:
		if request.method == 'POST':
			name = request.POST.get('name')

			description = request.POST.get('description')
			date_finish = request.POST.get('finish_date')
			Species_project.objects.create(name=name, description = description, finish_task=date_finish)
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
		project_select = Project.objects.filter(id = pk)
		project_for_form = Project.objects.get(id = pk)

		if request.method == 'POST':
			species_project_id = request.POST.get('species_project_id')
			name = request.POST.get('name')
			description = request.POST.get('description')
			species_task = request.POST.get('species_task')
			date_finish = request.POST.get('finish_date')
			user_task = request.POST.getlist('user_task')


			for items in project_select:

				items.name = name
				items.species_id = species_project_id
				items.species_task_id = species_task
				items.finish_task = date_finish
				items.description = description
				items.complete_value = " "
				items.save()

			user_delete = UserProject.objects.filter(project = pk)
			user_delete.delete()
			for itm in user_task:
				user_main = UserProject.objects.create(project = project_select[0], user_id = int(itm))

			return redirect('/project/'+species_project_id)

		return render(request, 'projects/update_project_task.html', {'task_species': task_species, 'user_list': user_list, 'project_select': project_for_form})



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
		project = Project.objects.filter(id = pk)

		for itm in project:
			itm.complete_value = 1
			itm.save()
		speci = str(itm.species_id)
		return redirect('/project/'+speci)
