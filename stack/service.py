from django.db import connection
import datetime

def authenticate(username,password):

	cursor = connection.cursor()
	cursor.execute("select * from employee where user_name = %s and password = %s",[username,password])
	row = cursor.fetchall()
	if len(row) ==1:
		return row[0]
	else:
		return False

def createIssue(title,description,created_user):
	cursor=connection.cursor()
	date = datetime.datetime.now()
	cursor.execute(" insert into issue(title, description, created_date, created_by) values(%s,%s,%s,%s) ", [title,description,date,created_user])
	connection.commit()

def getIssues():
	cursor = connection.cursor()
	# cursor.execute(" select * from issue ")
	cursor.execute("select id,title,description from issue")
	val = cursor.fetchall()
	rowList = []
	for row in val:
		rowdict = {'id':row[0],'title':row[1],'description':row[2]}
		rowList.append(rowdict)
	return rowList

def getIssueById(id): #,created_user_id
	cursor = connection.cursor()
	cursor.execute(" select a.id,first_name,last_name,title,description,created_date from issue a join employee b on a.created_by = b.id where a.id = %s",[id])
	#cursor.execute(" select * from issue where id = %s ", [id])
	row = cursor.fetchone()
	return row

def createSolution(solution, created_user, issue_id):

	cursor = connection.cursor()
	date = datetime.datetime.now()
	cursor.execute(" insert into solution (solution, created_by, created_date, issue_id) values(%s,%s,%s,%s)",[solution,created_user,date,issue_id])
	connection.commit()
	
def getSolutionsForIssue(issue_id):
	cursor = connection.cursor()

	#cursor.execute(" select first_name,last_name,solution,created_date from solution,employee where  issue_id = %s", [issue_id])
	cursor.execute(" select first_name,last_name,solution,created_date from solution a,employee b where a.created_by = b.id and issue_id = %s", [issue_id])
	#cursor.execute(" select * from solution where issue_id = %s", [issue_id])
	row = cursor.fetchall()
	return row

def getSearchResult(searchKey):
	cursor = connection.cursor()
	searchKey = '%'+searchKey+'%'
	cursor.execute(" select id,title, description from issue where title like %s or description like %s",[searchKey,searchKey])
	searchResult = cursor.fetchall()
	
	rowList = []
	for row in searchResult:
		rowdict = {'id':row[0],'title':row[1],'description':row[2]}

		rowList.append(rowdict)
	print rowList	
	return rowList
	# #print searchResult{'id':=id,'title':=title,'description':description}
	# print searchResult,'resul....'
	# return searchResult

	




	
