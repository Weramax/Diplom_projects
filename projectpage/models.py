from django.db import models


class Species_Task(models.Model):
	name = models.CharField(max_length = 250)
	description = models.TextField()

	def __str__(self):
		return self.name


class Species_project(models.Model):
	name = models.CharField(max_length=250)
	description = models.TextField()

	def __str__(self):
		return self.name

class Project(models.Model):

    name = models.CharField(max_length = 250)
    
    species = models.ForeignKey('Species_project', on_delete = models.CASCADE)

    species_task = models.ForeignKey('Species_Task', on_delete = models.CASCADE)

    description = models.TextField()

    def __str__(self):
    	return self.name

   