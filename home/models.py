from django.db import models

class Student(models.Model):    
    usn = models.CharField(max_length=100)
    sname = models.CharField(max_length=100,null=True)
    sem = models.IntegerField(null=True)
    department = models.CharField(max_length=100,null=True)

    def __str__(self):
            return self.usn 
   

class Teacher(models.Model):
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
    # pfile = models.FileField() 
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
    
    comment = models.TextField(null=True, blank=False)
    likes = models.IntegerField(null=True, blank=False)

    best_project = (
        ('Y','Yes'),
        ('N','No')
    )
    best_project = models.CharField(max_length=5,choices=best_project,default='N')

    def __str__(self):
            return self.pname
   
    
