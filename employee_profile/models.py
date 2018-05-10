from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
	employee = models.ForeignKey(User, on_delete=models.CASCADE)
	is_employee = models.BooleanField(default=False)
	

class Admin(models.Model):
	admin = models.ForeignKey(User, on_delete=models.CASCADE)
	is_admin = models.BooleanField(default=False)



class Assignment(models.Model):
	title = models.CharField(max_length=100,null=True)
	description = models.CharField(max_length=80,null=True)
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True)
	status = models.CharField(max_length=50,null=True)

class Day(models.Model):
	day = models.CharField(max_length=50)
	employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)

class Grade(models.Model):
	grade = models.CharField(max_length=80)
	employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)


	



