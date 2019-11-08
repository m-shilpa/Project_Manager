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
