from django.conf.urls import url

from .views import main, details, create_project, create_project_task, GeneratePDF

urlpatterns = [
	url(r'^$', main),
	url(r'^project/(?P<pk>\d+)$', details),
	url(r'^project/createproject$', create_project),
	url(r'^(?P<pk>\d+)/create_project_task$', create_project_task),
	url(r'^(?P<pk>\d+)/pdf/$', GeneratePDF.as_view())
]