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
	try:
		project = Project.objects.filter(student_id = Student.objects.get(user = name))
	except:
		return HttpResponse('You dont have  any project')
	print(project)
	return render(request,'mysubmission.html',{'projects':project})

def home(request):
	branches = { i[0]:i[1] for i in Project.Branch}
	return render(request,'home.html',{'branches':branches})




	
def teachersignin(request):
	correct = 1
	if request.method == 'POST':
		user = request.POST.get('user')
		password = request.POST.get('password')
		
		user = authenticate(request, username=user, password=password)
		if user is not None:
			print(user)
			login(request, user)
			return redirect("/teacherlist")
		else:
			correct = 0
			return render(request, 'teachersignin.html',{'correct' : correct})

	return render(request, 'teachersignin.html', {'correct' : correct})


def teachersignup(request):
	if request.method == 'POST':
		tname = request.POST.get('tname',None)
		email = request.POST.get('email',None)
		dept = request.POST.get('dept',None)
		domain = request.POST.get('domain',None)
		yearsofexperience = request.POST.get('yearsofexperience',None)
		position = request.POST.get('position',None)
		password = request.POST.get('password',None)
		if User.objects.filter(email=email).exists():
			return HttpResponse('User already exists')
		else:
			user = User.objects.create_user(username=email,email = email, password = password)
			user.save()
			teacher = Teacher(user = user, tname = tname, dept = dept, domain = domain, yearsofexperience = yearsofexperience, position = position)
			teacher.save()
			login(request, user)
			return redirect("/")
	return render(request, 'teachersignup.html')
	
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

	project = Project.objects.get(pk=pid)
	print(project)
	return render(request,"teacherview.html",{'project':project})

def teacherlist(request):
	
	
	try:
		teacher = Teacher.objects.get(user = request.user)
		projects = Project.objects.filter(teacher_id =teacher , status='U')
		return render(request,"teacherlist.html",{'projects':projects})
	except:
		return HttpResponse("You do not have access to this page")
	
	

# def teacherlist1(request):
# 	teacher = Teacher.objects.all()
# 	if request.user not in teacher:
# 		return HttpResponse("You do not have access to this page")
# 	else:
# 		teacher = request.user
# 		projects = Project.objects.filter(teacher_id =Teacher.objects.get(user = teacher) , status='U')
# 		return render(request,"teacherlist.html",{'projects':projects})

def deptProjects(request,dept):

	projects = Project.objects.filter(branch=dept,types = "Re") #Type = report,status = accepted, branch
	domain = projects.values('domain').distinct() #domain for that department
	sem = projects.values('sem').distinct() # sem for that department
	subject = projects.values('subject').distinct() #subjects for that department

	if request.method =='POST':
		domain1 = request.POST.get('domain',None)
		subject1 = request.POST.get('subject',None)
		sem1 = request.POST.get('sem',None)
		if domain1!=None:
			projects = projects.filter(domain = domain1)
		if subject1!=None:
			projects = projects.filter(subject = subject1)
		if sem1!=None:
			projects = projects.filter(sem = sem1)
			print(projects,domain1)
			return render(request,'deptProjects.html',{'projects':projects,'domains':domain,'sems':sem,'subjects':subject})
		 

	
	return render(request,'deptProjects.html',{'projects':projects,'domains':domain,'sems':sem,'subjects':subject})

def project(request,pid):
	project = list(Project.objects.filter(id=pid))
	comment = list(Comment.objects.filter(project=pid))
	print("user------------------",request.user)
	if request.method =='POST':
		user_comment = request.POST.get('comment',None)
		project1 = Project.objects.get(id=pid)
		comment = Comment(comment=user_comment,project=project1,user = request.user)
		comment.save()
		comment_list = list(Comment.objects.filter(project=pid))
		return render(request,"project.html",{'project': project[0], 'comments':comment_list})
	return render(request,"project.html",{'project': project[0], 'comments':comment})
