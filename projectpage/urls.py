from django.conf.urls import url

from .views import main, details, create_project, create_project_task, generate_pdf, delete_project_task, update_project_task, details_user,complete_task

urlpatterns = [
	url(r'^$', main),
	url(r'^project/(?P<pk>\d+)$', details),
	url(r'^project/createproject$', create_project),
	url(r'^(?P<pk>\d+)/create_project_task$', create_project_task),
	url(r'^(?P<pk>\d+)/pdf/$', generate_pdf),
	url(r'^(?P<pk>\d+)/deleteprojectsk', delete_project_task),
	url(r'^(?P<pk>\d+)/update_project_task$', update_project_task),
	url(r'^project/my-project$', details_user),
	url(r'^(?P<pk>\d+)/compete_task', complete_task)
]