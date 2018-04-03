from django.db import models

class Species_Task(models.Model):
	name = models.CharField(max_length = 250)
	description = models.TextField()

	def __str__(self):
		return self.name


class Species_project(models.Model):
	name = models.CharField(max_length=250)
	short_description = models.TextField()
	description = models.TextField()
	created_task = models.DateField(verbose_name='Дата создания',auto_now_add=True)
	finish_task = models.DateField(verbose_name='Дата окончания')

	def __str__(self):
		return self.name

class Project(models.Model):

    name = models.CharField(max_length = 250)
    
    species = models.ForeignKey('Species_project', on_delete = models.CASCADE)

    species_task = models.ForeignKey('Species_Task', on_delete = models.CASCADE)

    created_task = models.DateField(verbose_name='Дата создания',auto_now_add=True)

    finish_task = models.DateField(verbose_name='Дата окончания')
    
    description = models.TextField()

    def __str__(self):
    	return self.name


   