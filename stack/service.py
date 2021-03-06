from django.db import connection
import datetime

def authenticate(username,password): 

	cursor = connection.cursor()
	cursor.execute("select * from employee where user_name = %s and password = md5(%s)",[username,password])
	row = cursor.fetchall()

	if len(row) ==1: 
		row = row[0]
		rowdict = {'id':row[0],'first_name':row[1],'last_name':row[2],'emp_no':row[3],'user_name':row[4],'email':row[6],'is_active':row[7]} 
		return rowdict
	else:
		return False

def createIssue(title,description,created_user):
	cursor=connection.cursor()
	date = datetime.datetime.now()
	cursor.execute(" insert into issue(title, description, created_date, created_by) values(%s,%s,%s,%s) ", [title,description,date,created_user])
	connection.commit()

def getIssues(fromLimit,toLimit):
	cursor = connection.cursor()
	# cursor.execute(" select * from issue ") 
	cursor.execute("select first_name,last_name,b.id,title,description,created_date from employee a, issue b where a.id = b.created_by limit %s,%s",[fromLimit,toLimit])
	val = cursor.fetchall()
	rowList = []
	for row in val:
		rowdict = {'first_name':row[0],'last_name':row[1],'id':row[2],'title':row[3],'description':row[4],'created_date':row[5]}
		rowList.append(rowdict)
	return rowList

def totalRecord():
	cursor = connection.cursor()
	cursor.execute("select count(id) from issue")
	val = cursor.fetchall()
	return val[0][0]

def getIssueById(id): #,created_user_id
	cursor = connection.cursor()
	cursor.execute(" select a.id,first_name,last_name,title,description,created_date from issue a join employee b on a.created_by = b.id where a.id = %s order by a.id desc",[id])
	#cursor.execute(" select * from issue where id = %s ", [id])
	row = cursor.fetchone()
	rowdict = {'id':row[0],'first_name':row[1],'last_name':row[2],'title':row[3],'description':row[4],'created_date':row[5]}
	return rowdict

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
	solList = []
	allRow = cursor.fetchall()
	for row in allRow:
		rowdict = {'first_name':row[0],'last_name':row[1],'solution':row[2],'created_date':row[3]}
		solList.append(rowdict)
	return solList

def getSearchResult(searchKey,fromLimit,toLimit):
	print fromLimit,toLimit
	cursor = connection.cursor()
	sql = "select a.id,title, description, first_name, last_name,created_date from issue a join employee b on a.created_by = b.id "
	if searchKey != "":
		sql += "where"
	lowerSearchKey = searchKey.lower()
	string = lowerSearchKey.split()
	stringFinal = getKeyword(string)
	sqlList = []
	for index,splitWord in enumerate(stringFinal):
		likeKey = '%'+splitWord+'%'
		if index !=0:
			sql += ' or '
		sql += " title like %s or description like %s "

		sqlList.append(likeKey)
		sqlList.append(likeKey)
	cursor.execute(sql,sqlList)
	withoutLimitResult = cursor.fetchall()
	# todo : insted of taking whole record and counting, try to use count query for optimization
	a = len(withoutLimitResult)

	sql += "limit %s,%s"%(fromLimit,toLimit)
	cursor.execute(sql,sqlList)
		
	searchResult = cursor.fetchall()
	
	rowList = []
	for row in searchResult:
		rowdict = {'id':row[0],'title':row[1],'description':row[2],'first_name':row[3],'last_name':row[4],'created_date':row[5]}

		rowList.append(rowdict)
	print rowList,a
	return rowList,a

def getKeyword(finalString):
	print finalString
	removeList = ['a','is','was','we','and','when','what','as','where','to','at','for','at','in','i','be','that','this','have','has','had']
	finalList = []
	for row in finalString:		
		if row not in removeList:				
			finalList.append(row)
	return finalList	
		




	# #print searchResult{'id':=id,'title':=title,'description':description}
	# print searchResult,'resul....'
	# return searchResult 
# 	SQL=select * from table
# For sting in list:
# SQL += or description=%s

	




	
