from home.models import *
from django.contrib.auth import authenticate, login ,logout
from datetime import date
from django.shortcuts import render, HttpResponse, redirect, render_to_response 

def signout(request):
	logout(request)
	return redirect("/")

def studentsignin(request):
	correct = 1
	if request.method == 'POST':
		user = request.POST.get('user')
		password = request.POST.get('password')
		
		user = authenticate(request, username=user, password=password)
		if user is not None:
			print(user)
			login(request, user)
			return redirect("/")
		else:
			correct = 0
			return render(request, 'studentsignin.html',{'correct' : correct})

	return render(request, 'studentsignin.html', {'correct' : correct})

def studentsignup(request):
	if request.method == 'POST':
		name = request.POST.get('username',None)
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)
		usn = request.POST.get('usn',None)
		sem = request.POST.get('sem',None)
		dpt = request.POST.get('dpt', None)

		if User.objects.filter(email=email).exists():
			return HttpResponse('User already exists')
		else:
			user = User.objects.create_user(username=email,email = email, password = password)
			user.save()
			student = Student(user = user, usn = usn,sem = sem,department = dpt,sname = name)
			student.save()
			login(request, user)
			return redirect("/")
			
		
	return render(request, "studentsignup.html")

def home(request):
	return HttpResponse('Hi')

def teacherview(request,pid):
	if request.method == 'POST':
		sid = request.POST.get('sid')
		status = request.POST.get('status','U')
		comment = request.POST.get('comment',None)
		a = Project.objects.get(id=pid)
		a.status = status
		a.save()
		b= Comment(student = a.student_id,project = a,comment=comment)
		b.save()
		return redirect("/teacherlist")

	project = Project.objects.filter(id=pid).values('student_id','teacher_id','pname','domain','summary','subject','branch','pfile','sem','types','status')[0]
	return render(request,"teacherview.html",{'project':project})

def teacherlist(request):
	 
	projects = Project.objects.exclude(status='A')
	return render(request,"teacherlist.html",{'projects':projects})