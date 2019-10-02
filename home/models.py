from django.db import models

class Student(models.Model):    
    usn = models.CharField(max_length=100)
    sname = models.CharField(max_length=100,null=True)
    sem = models.CharField(max_length=100,null=True)
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
    summary = models.TextField(null=True)
    subject = models.CharField(max_length = 100)
    # pfile = models.FileField() 

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
    
    comment = models.TextField(null=True)
    likes = models.IntegerField(null=True)

    best_project = (
        ('1','Yes'),
        ('0','No')
    )
    best_project = models.IntegerField(choices=best_project,default=0)

    def __str__(self):
            return self.pname
   

