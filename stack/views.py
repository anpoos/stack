from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from stack.service import authenticate, dataStore, getIssues, getIssueById, solutionStore
#from django.views.generic import TemplateView
def login(request):
	if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']

          user = authenticate(username = username,password = password)
          if user:
          	request.session['logged_user'] = user
          	return HttpResponseRedirect('/home')
         
              
      
	return render_to_response('login.html',)

	# if request.POST:
	# 	username = request.POST['username']
 #    	password = request.POST['password']
	#return render_to_response('login.html')

def home(request):
	record = getIssues()
	print record
	return render_to_response('home.html',{'record':record})
def createIssue(request):

	if request.method == 'POST':
		title = request.POST['title']
		description = request.POST['description']
		created_user_id = request.session['logged_user'][0]
		store = dataStore(title,description,created_user_id)
	return render_to_response('issue.html')

def viewIssue(request,id):
	
	issue = getIssueById(id)
	if request.method == 'POST':
		solution = request.POST['solution']
	return render_to_response('view_issue.html',{'issue':issue})

def viewSolution(request,id):
	
	if request.method =='POST':
		solution = request.POST['solution']
		created_user_id = request.session['logged_user'][0]
		print created_user_id
		store = solutionStore(solution,created_user_id,id)
	return render_to_response('view_issue.html',{'store':store})	


	
