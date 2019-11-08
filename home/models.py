from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):    
    user = models.OneToOneField(User,  on_delete=models.CASCADE ) #required for authentication. Django allows authentication for users field only
    sname = models.CharField(max_length = 100)
    usn = models.CharField(max_length=100)
    sem = models.IntegerField(null=True)
    department = models.CharField(max_length=100,null=True) #branch

    def __str__(self):
            return self.usn 
   

class Teacher(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    tname = models.CharField(max_length = 100)
    dept = models.CharField(max_length=100)
    domain = models.CharField(max_length=100,null=True)
    yearsofexperience = models.IntegerField(null=True)
    position = models.CharField(max_length=100)  # is he a hod or professor etc

    def __str__(self):
            return self.tname
   
   

class Project(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    teacher_id = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True)
    pname = models.CharField(max_length = 100)
    domain = models.CharField(max_length = 100,null=True)
    summary = models.TextField(null=True, blank=False)
    subject = models.CharField(max_length = 100, blank=False)
    branch =  (
        ('CS','Computer Science'),
        ('IS','Information Science'),
        ('EC', 'Electronics'),
        ('CIVIL', 'Civil'),
        ('MECH','mechanical'),
        ('EEE', 'eee'),
        ('IE', 'ie'),
        ('TC', 'TC')
    )
    branch = models.CharField(max_length = 50, choices = branch)
    pfile = models.FileField(upload_to='home/pfiles', max_length=1000, null = True)
    sem = models.IntegerField(null=True)
    project_pic= models.ImageField(upload_to='home/images', default='home/images/dummyimage.PNG', blank=False)
    types = (
        ('Sy','synopis'),
        ('Re','report')
    )
    types = models.CharField(max_length=5,choices=types) 

    status = (
        ('A','accepted'),
        ('R','rejected'),
        ('M','modify'),
        ('U','unseen')
    )
    status = models.CharField(max_length=5,choices=status,default='U')
    
    
    likes = models.IntegerField(null=True, blank=False)

    best_project = (
        ('Y','Yes'),
        ('N','No')
    )
    best_project = models.CharField(max_length=5,choices=best_project,default='N')


    def __str__(self):
            return self.pname

class Comment(models.Model):
      student = models.ForeignKey(Student,on_delete=models.CASCADE)
      project = models.ForeignKey(Project,on_delete=models.CASCADE)
      comment = models.TextField(null=True)
      def __str__(self):
          return self.project.pname
      
