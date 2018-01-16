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
	cursor.execute(" select * from issue ")
	val = cursor.fetchall()
	return val

def getIssueById(id):
	cursor = connection.cursor()
	cursor.execute(" select * from issue where id = %s ", [id])
	row = cursor.fetchone()
	return row

def createSolution(solution, created_user, issue_id):
	print id, created_user
	cursor = connection.cursor()
	date = datetime.datetime.now()
	print created_user
	cursor.execute(" insert into solution (solution, created_by, created_date, issue_id) values(%s,%s,%s,%s)",[solution,created_user,date,issue_id])
	connection.commit()
	
def getSolutionsForIssue(issue_id):
	cursor = connection.cursor()
	cursor.execute(" select * from solution where issue_id = %s", [issue_id])
	row = cursor.fetchall()
	return row


	