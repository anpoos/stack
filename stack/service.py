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
	cursor.execute("select first_name,last_name,b.id,title,description,created_date from employee a, issue b where a.id = b.created_by")
	val = cursor.fetchall()
	rowList = []
	for row in val:
		rowdict = {'first_name':row[0],'last_name':row[1],'id':row[2],'title':row[3],'description':row[4],'created_date':row[5]}
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
	print row
	return row

def getSearchResult(searchKey):
	cursor = connection.cursor()
	sql = "select id,title, description from issue where "
	string = searchKey.split()
	stringFinal = getKeyword(string)
	sqlList = []
	for index,splitWord in enumerate(stringFinal):
		searchKey = '%'+splitWord+'%'
		if index !=0:
			sql += ' or '
		sql += " title like %s or description like %s "
		sqlList.append(searchKey)
		sqlList.append(searchKey)

	cursor.execute(sql,sqlList)
		
	searchResult = cursor.fetchall()
	
	rowList = []
	for row in searchResult:
		rowdict = {'id':row[0],'title':row[1],'description':row[2]}

		rowList.append(rowdict)
		print rowList	
	return rowList

def getKeyword(string):
	print string
	removeList = ['a','is','was','and','when','what','as','where','to','at']
	finalList = []
	for row in string:		
		if row not in removeList:				
			finalList.append(row)
	return finalList	
		




	# #print searchResult{'id':=id,'title':=title,'description':description}
	# print searchResult,'resul....'
	# return searchResult 
# 	SQL=select * from table
# For sting in list:
# SQL += or description=%s

	




	
