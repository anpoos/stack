from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from stack import service
#from django.views.generic import TemplateView
def login(request):
	if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']

          user = service.authenticate(username = username,password = password)
          if user:
          	request.session['logged_user'] = user
          	print request.session['logged_user']
          	return HttpResponseRedirect('/')
                      
	return render_to_response('login.html',)

def logout(request):
	if 'logged_user' in request.session:
		del request.session['logged_user']
	return HttpResponseRedirect('/login')


def home(request):
	if not 'logged_user' in request.session:
		return HttpResponseRedirect('/login')
	record = service.getIssues()
	print record
	return render_to_response('home.html',{'record':record})

def create(request):
	if not 'logged_user' in request.session:
		return HttpResponseRedirect('/login')	
	if request.method == 'POST':
		title = request.POST['title']
		description = request.POST['description']
		created_user_id = request.session['logged_user'][0]


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
		created_user_id = request.session['logged_user'][0]
		store = service.createSolution(solution,created_user_id,id)
	return HttpResponseRedirect('/view_issue/%s'%(id))	

def searchResult(request):
	if not 'logged_user' in request.session:
		return HttpResponseRedirect('/login')
	if request.method == 'POST':
		searcKey = request.POST['search']
		query = service.getSearchResult(searcKey)
		return render_to_response('home.html',{'record':query})
	return render_to_response('home.html')

