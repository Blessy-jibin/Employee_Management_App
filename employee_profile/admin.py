from django.contrib import admin

from .models import Employee,Admin,Assignment,Day,Grade
myModels = [Employee,Admin,Assignment,Day,Grade]
admin.site.register(myModels)


