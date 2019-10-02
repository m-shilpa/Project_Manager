from django.contrib import admin
from .models import Student,Teacher,Project

# username:admin, password:admin1234.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Project)


