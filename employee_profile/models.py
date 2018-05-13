from django.db import models
from django.contrib.auth.models import User

class Day(models.Model):
	day = models.CharField(max_length=50)

	def __str__(self):
		return self.day

class Grade(models.Model):
	grade = models.CharField(max_length=50)

	def __str__(self):
		return self.grade

class Employee(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	is_admin = models.BooleanField(default=False)
	days = models.ManyToManyField(Day)
	grades = models.ManyToManyField(Grade)

	def __str__(self):
		return '%s %s %s' % (self.user.username, self.days, self.grades)

class Admin(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	is_admin = models.BooleanField(default=False)

	def __str__(self):
		return self.admin

class Assignment(models.Model):
	title = models.CharField(max_length=100,null=True)
	description = models.CharField(max_length=80,null=True)
	start_date = models.CharField(max_length=20,null=True)
	end_date = models.CharField(max_length=20,null=True)
	employee = models.ForeignKey(Employee,on_delete=models.CASCADE,)
	status = models.CharField(max_length=50,null=True)

	def __str__(self):
		return self.title
	

	



