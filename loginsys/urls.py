from django.conf.urls import url,  include

from .views import LoginFormView, LogoutView

urlpatterns = [
	url(r'^login/$', LoginFormView.as_view()),
	url(r'^logout/$', LogoutView.as_view())

]