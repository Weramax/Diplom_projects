from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class Species_Task(models.Model):
	name = models.CharField(max_length = 250)
	description = models.TextField()

	def __str__(self):
		return self.name


class Species_project(models.Model):
	name = models.CharField(max_length=250)
	description = models.TextField()
	created_task = models.DateField(verbose_name='Дата создания',auto_now_add=True)
	finish_task = models.DateField(verbose_name='Дата окончания')
	progress_value = models.IntegerField(verbose_name="Процент завершения", default=0)

	def __str__(self):
		return self.name


class Documents(models.Model):
	name = models.CharField(max_length=50)
	species = models.ForeignKey('Species_project', on_delete=models.CASCADE)
	file = models.FileField(upload_to="documents/%Y/%m/%d")

class Project(models.Model):
	name = models.CharField(max_length = 250)
	complete_value = models.CharField(max_length=1, default="0")
	species = models.ForeignKey('Species_project', on_delete = models.CASCADE)
	species_task = models.ForeignKey('Species_Task', on_delete = models.CASCADE)
	created_task = models.DateField(verbose_name='Дата создания',auto_now_add=True)
	finish_task = models.DateField(verbose_name='Дата окончания')
	user = models.ManyToManyField(User, through='UserProject')
	description = models.TextField()
	class Meta:
		ordering = ['finish_task']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return "/"

class UserProject(models.Model):
	project = models.ForeignKey(Project, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)


class Comment(models.Model):
	class Meta:
		db_table = "comments"

	project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
	author_id = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField('Комментарий', max_length=500)
	pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)


