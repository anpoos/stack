from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from stack import service
import math
import os

#from django.views.generic import TemplateView

def signUp(request):
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		empno = request.POST['empno']
		username = request.POST['username']
		password = request.POST['password']
		emailid = request.POST['emailid']
		insert = service.empDetails(firstname,lastname,empno,username,password,emailid)
		return HttpResponseRedirect('/login')

	return render_to_response('sign_up.html')
	

def login(request):
	if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']

          user = service.authenticate(username = username,password = password)
          if user: 
          	request.session['logged_user'] = user
          	return HttpResponseRedirect('/')
                      
	return render_to_response('login.html',)

def logout(request):
	if 'logged_user' in request.session:
		del request.session['logged_user']
	return HttpResponseRedirect('/login')


def home(request):
	if not 'logged_user' in request.session:
		return HttpResponseRedirect('/login')
	
	limit = 3
	pageNo = request.GET.get('page',1)
	start = (int(pageNo)-1)*limit
	#query = service.getIssues(start,limit)
	#recordCount= service.totalRecord()
	#pageCount = int(math.ceil(recordCount/float(limit)))
	if request.method == 'GET':
		searcKey = request.GET.get('search',"")

		query,recordCount = service.getSearchResult(searcKey,start,limit)
		pageCount = int(math.ceil(recordCount/float(limit)))
		return render_to_response('home.html',{'record':query,'currentPgNo':pageNo,'pageCount':pageCount,'searchValue':searcKey,})
	#pageCountList=range(1,pageCount+1) #convert integer/float to list; eg:range(2)=>[0,1] // not needed

def create(request):
	if not 'logged_user' in request.session:
		return HttpResponseRedirect('/login')	

	if request.method == 'POST':
		title = request.POST['title']
		description = request.POST['description']
		try:
			img_obj = request.FILES['attachment']
		except:
			img_obj = ""
		created_user_id = request.session['logged_user']['id']
		upload_dir = "static/img_issue/"
		try:
			fout = open(os.path.join(upload_dir,img_obj.name),'wb')
			fout.write(img_obj.read())
		except:
			pass
		store = service.createIssue(title,description,img_obj,created_user_id)
	return render_to_response('issue.html')

def viewIssue(request,id):
	if not 'logged_user' in request.session:
		return HttpResponseRedirect('/login')
	#created_user_id = request.session['logged_user'][0] # for accessing  user name by id
	issue = service.getIssueById(id)#,created_user_id
	solutions = service.getSolutionsForIssue(id)

	return render_to_response('view_issue.html',{'issue':issue,'solutions':solutions})

def setSolution(request,id):
	if not 'logged_user' in request.session:
		return HttpResponseRedirect('/login')
	
	if request.method =='POST':
		solution = request.POST['solution']
		try:
			img_obj = request.FILES['attachment']
		except:
			img_obj = ""
		created_user_id = request.session['logged_user']['id']
		upload_dir = "static/img_solution/"
		try:
			fout = open(os.path.join(upload_dir,img_obj.name),'wb')
			fout.write(img_obj.read())
		except:
			pass

		store = service.createSolution(solution,img_obj,created_user_id,id)
	return HttpResponseRedirect('/view_issue/%s'%(id))	

def edit(request):
	if not 'logged_user' in request.session:
		return HttpResponseRedirect('/login')
	created_user_id = request.session['logged_user']['id']
	query = service.myIssue(created_user_id)
	return render_to_response('home.html',{'record':query,})

def editIssue(request,id):
	created_user_id = request.session['logged_user']['id']
	editable_issue = service.showEditableIssue(id,created_user_id)
	if editable_issue:
		if request.method == 'POST':
			title = request.POST['title']
			description = request.POST['description']
			try:
				img_obj = request.FILES['attachment']
			except:
				img_obj = ""
			created_user_id = request.session['logged_user']['id']
			upload_dir = "static/img_issue/"
			try:
				fout = open(os.path.join(upload_dir,img_obj.name),'wb')
				fout.write(img_obj.read())
			except:
				pass
			store = service.updateIssue(title,description,img_obj,id)
		return render_to_response('issue.html',{'issue':editable_issue,})
	else:
		return HttpResponseRedirect('/')



# def searchResult(request):
# 	if not 'logged_user' in request.session:
# 		return HttpResponseRedirect('/login')
# 	limit = 10
# 	pageNo = request.GET.get('page',1)
# 	start = int(pageNo)*limit-(limit-1)
# 	recordCount= service.totalRecord()
# 	pageCount = int(math.ceil(recordCount/float(limit)))
# 	if request.method == 'GET':
# 		searcKey = request.GET['search']
# 		query = service.getSearchResult(searcKey,start,limit)
# 		return render_to_response('home.html',{'record':query,'currentPgNo':pageNo,'pageCount':pageCount,'searchValue':searcKey,})
# 	return render_to_response('home.html')

