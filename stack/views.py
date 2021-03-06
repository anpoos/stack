from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from stack import service
import math
#from django.views.generic import TemplateView
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
	#record = service.getIssues(start,limit) 
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
		created_user_id = request.session['logged_user']['id']


		store = service.createIssue(title,description,created_user_id)
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
		created_user_id = request.session['logged_user']['id']
		store = service.createSolution(solution,created_user_id,id)
	return HttpResponseRedirect('/view_issue/%s'%(id))	

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

