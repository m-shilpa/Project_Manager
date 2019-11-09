from django.contrib import admin
from .models import Student,Teacher,Project,Comment

# username:shilpa, password:shilpa123
#user:  teacher1, pass:shilpa123

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Project)
admin.site.register(Comment)

