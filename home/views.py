from home.models import *
from django.contrib.auth import authenticate, login ,logout
from datetime import date
from django.shortcuts import render, HttpResponse, redirect, render_to_response 




def signout(request):
	logout(request)
	return redirect("/")

# ----------------------------------------Student Login-----------------------------------

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
		usn = request.POST.get('usn',None).upper()
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



# ----------------------------------------Student Report Sumbmission-------------------------------------------------

def submit(request):
	if request.method == 'POST':
		usn = request.POST.get('usn',None).upper()
		teacher_id = request.POST.get('teacher', None)
		pname = request.POST.get('pname', None)
		domain = request.POST.get('domain', None)
		summary = request.POST.get('summary', None)
		subject = request.POST.get('subject', None)
		pfile = request.FILES.get('pfile', None)
		project_pic = request.FILES.get('project_pic',None)
		types = request.POST.get('types', None)
		
		print(pfile,project_pic)
		try:
			student = Student.objects.get(usn = usn)
			branch = student.department
			sem = student.sem

		
		except:
			return HttpResponse('Student doesnot exists')


		
		project = Project(student_id = student,pname=pname,domain = domain,summary = summary,subject = subject,branch = branch,pfile = pfile,sem = sem,project_pic = project_pic, types = types )
		project.save()
		

	teachers = Teacher.objects.all()
	return render(request, "submit.html", {'teachers':teachers})

def update(request,project_id):
	project = Project.objects.get(pk = project_id)
	teachers = Teacher.objects.all()
	if request.method == 'POST':
		
		
		project.pname = request.POST.get('pname', None)
		project.domain = request.POST.get('domain', None)
		project.summary = request.POST.get('summary', None)
		project.subject = request.POST.get('subject', None)
		pfile = request.FILES.get('pfile', None)
		if pfile is not None:
			project.pfile = pfile
		pic = request.FILES.get('project_pic',None)
		if project is not None:
			project.projet_pic = pic

		project.types = request.POST.get('types', None)	
		project.save()

	
	
	return render(request,"update.html",{'project': project, 'teachers':teachers })

def mysubmission(request):
	name = request.user
	project = Project.objects.filter(student_id = Student.objects.get(user = name))
	print(project)
	return render(request,'mysubmission.html',{'projects':project})

def home(request):
	branches = { i[0]:i[1] for i in Project.Branch}
	return render(request,'home.html',{'branches':branches})

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
	projects = Project.objects.filter(teacher_id =1 , status='U')
	return render(request,"teacherlist.html",{'projects':projects})

def teacherlist1(request):
	teacher = Teacher.objects.all()
	if request.user not in teacher:
		return HttpResponse("You do not have access to this page")
	else:
		teacher = request.user
		projects = Project.objects.filter(teacher_id =Teacher.objects.get(user = teacher) , status='U')
		return render(request,"teacherlist.html",{'projects':projects})

def deptProjects(request,dept):

	projects = Project.objects.filter(branch=dept)
	domain = Project.objects.values('domain')
	sem = Project.objects.values('sem')
	subject = Project.objects.values('subject')

	# if request.method =='POST':
	# 	domain1 = request.POST.get('domain')
	# 	subject1 = request.POST.get('subject')
	# 	sem1 = request.POST.get('sem')
	# 	if domain1!=None and subject1==None and sem1==None:
	# 		projects = Project.objects.filter(branch=dept,domain=domain1)
	# 		return render(request,'deptProjects.html',{'projects':projects,'domains':domain,'sems':sem,'subjects':subject})
		 

	
	return render(request,'deptProjects.html',{'projects':projects,'domains':domain,'sems':sem,'subjects':subject})

def project(request,pid):
	return HttpResponse("hi")