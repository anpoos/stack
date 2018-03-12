from django.db import connection
import datetime
from stack import static_word
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from HTMLParser import HTMLParser


def empDetails(firstname,lastname,empno,username,password,emailid):
	cursor = connection.cursor()
	insert = cursor.execute(" insert into employee( first_name,last_name,emp_no,user_name,password,email ) values(%s,%s,%s,%s,md5(%s),%s) ",[firstname,lastname,empno,username,password,emailid])
	connection.commit()
	if insert:
		return insert
	else:
		return False

	

def authenticate(username,password):
	cursor = connection.cursor()
	cursor.execute("select * from employee where user_name = %s and password = md5(%s) and is_active = 1",[username,password])
	row = cursor.fetchall()

	if len(row) ==1: 
		row = row[0]
		rowdict = {'id':row[0],'first_name':row[1],'last_name':row[2],'emp_no':row[3],'user_name':row[4],'email':row[6],'is_active':row[7]} 
		return rowdict
	else:
		return False

def createIssue(title,description,image,created_user,send_mail=True):
	cursor=connection.cursor()
	date = datetime.datetime.now()

	inserted = cursor.execute(" insert into issue(title, description,image, created_date, created_by) values(%s,%s,%s,%s,%s) ", [title,description,image,date,created_user])
	if send_mail:
		all_mailid = getEmailsOfAll()
		logedUserName = getUserById(created_user)
		connection.commit()
		# send mail to all user when issue posted in issue stack
		fromaddr = static_word.mail_id
		toaddr = all_mailid
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		#msg['To'] = toaddr
		msg['Subject'] = "New Issue posted in Issue Stack"
		body = "The new issue is posted in Issue Stack its Title is <strong> %s </strong> and Description is <strong> %s </strong> by %s %s, Kindly login and prove your talent..."%(title,description,logedUserName['first_name'] ,logedUserName['last_name'])
		msg.attach(MIMEText(body, 'html'))
		server = smtplib.SMTP(static_word.host, static_word.port)
		server.starttls()
		server.login(fromaddr, static_word.pwd)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
		
	if inserted:
		return inserted
	else:
		return False
	

def getIssues(fromLimit,toLimit):
	cursor = connection.cursor()
	# cursor.execute(" select * from issue ") 

	cursor.execute("select first_name,last_name,b.id,title,description,created_date from employee a, issue b where a.id = b.created_by limit %s,%s",[fromLimit,toLimit])
	val = cursor.fetchall()
	rowList = []
	for row in val:
		rowdict = {'first_name':row[0],'last_name':row[1],'id':row[2],'title':row[3],'description':row[4],'created_date':row[5]}
		rowList.append(rowdict)
	if rowList:
		return rowList
	else:
		return False


def totalRecord():
	cursor = connection.cursor()
	cursor.execute("select count(id) from issue")
	val = cursor.fetchall()
	return val[0][0]

def getIssueById(id): #,created_user_id
	cursor = connection.cursor()
	cursor.execute(" select a.id,first_name,last_name,title,description,image,created_date from issue a join employee b on a.created_by = b.id where a.id = %s order by a.id desc",[id])
	#cursor.execute(" select * from issue where id = %s ", [id])
	row = cursor.fetchone()
	rowdict = {'id':row[0],'first_name':row[1],'last_name':row[2],'title':row[3],'description':row[4],'image':row[5],'created_date':row[6]}
	if rowdict:
		return rowdict
	else:
		return False

def createSolution(solution,img_obj,created_user,issue_id):
	cursor = connection.cursor()
	date = datetime.datetime.now()
	solutionRecord = cursor.execute(" insert into solution (solution,image,created_by, created_date, issue_id) values(%s,%s,%s,%s,%s)",[solution,img_obj,created_user,date,issue_id])
	all_mailid = getEmailsOfAll()
	logedUserName = getUserById(created_user)
	connection.commit()

	
	# send mail to all user when solution posted in issue stack
	fromaddr = static_word.mail_id
	toaddr = all_mailid
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	#msg['To'] = listOf_mail
	msg['Subject'] = "New Solution posted in Issue Stack for issue ID %s" %issue_id
	body = "The new solution for issue ID <strong> %s </strong> is <strong> %s </strong> by %s %s"%(issue_id,solution,logedUserName['first_name'] ,logedUserName['last_name'] )
	msg.attach(MIMEText(body, 'html'))
	server = smtplib.SMTP(static_word.host, static_word.port)
	server.starttls()
	server.login(fromaddr, static_word.pwd)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

	if solutionRecord:
		return solutionRecord
	else:
		return False

def getEmailsOfAll():
	cursor = connection.cursor()
	cursor.execute("select email from employee")
	mail_ids = cursor.fetchall()
	list_of_mails=[]
	for mail_id in mail_ids:
		list_of_mails.append(mail_id)
	return list_of_mails

def getUserById(id):
	cursor = connection.cursor()
	cursor.execute("select first_name,last_name from employee where id = %s",[id])
	result = cursor.fetchall()
	logedUserName = None
	for row in result:
		logedUserName = {'first_name':row[0],'last_name':row[1]}
	return logedUserName


def getSolutionsForIssue(issue_id):
	cursor = connection.cursor()

	#cursor.execute(" select first_name,last_name,solution,created_date from solution,employee where  issue_id = %s", [issue_id])
	cursor.execute(" select first_name,last_name,solution,image,created_date from solution a,employee b where a.created_by = b.id and issue_id = %s", [issue_id])
	#cursor.execute(" select * from solution where issue_id = %s", [issue_id])
	solList = []
	allRow = cursor.fetchall()
	for row in allRow:
		rowdict = {'first_name':row[0],'last_name':row[1],'solution':row[2],'image':row[3],'created_date':row[4]}
		solList.append(rowdict)
	return solList

def getSearchResult(searchKey,fromLimit,toLimit):
	cursor = connection.cursor()
	sql = "select a.id,title, description, first_name, last_name,created_date from issue a join employee b on a.created_by = b.id "
	if searchKey != "":
		sql += "where"
	#lowerSearchKey = searchKey.lower()
	#string = lowerSearchKey.split()
	stringFinal = getKeyword(searchKey)
	sqlList = []
	for index,splitWord in enumerate(stringFinal):
		likeKey = '%'+splitWord+'%'
		if index !=0:
			sql += ' or '
		sql += " title like %s or description like %s or first_name like %s or last_name like %s "

		sqlList.append(likeKey)
		sqlList.append(likeKey)
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
	return rowList,a

def getKeyword(finalString):
	lowerCaseSting = finalString.lower()
	splitedString = lowerCaseSting.split()
	removeList = ['a','is','was','we','and','when','what','as','where','to','at','for','at','in','i','be','that','this','have','has','had']
	finalList = []
	for row in splitedString:		
		if row not in removeList:				
			finalList.append(row)
	return finalList	
		
def myIssue(created_user_id):
	cursor = connection.cursor()
	cursor.execute("select first_name,last_name,b.id,title,description,created_date from employee a, issue b where a.id = b.created_by and b.created_by = %s",[created_user_id])
	val = cursor.fetchall()
	rowList = []
	for row in val:
		rowdict = {'first_name':row[0],'last_name':row[1],'id':row[2],'title':row[3],'description':row[4],'created_date':row[5]}
		rowList.append(rowdict)
	if rowList:
		return rowList
	else:
		return False
def showEditableIssue(issue_id,created_user_id):
	cursor = connection.cursor()
	cursor.execute("select title,description from issue where id = %s and created_by = %s",[issue_id,created_user_id])
	issues = cursor.fetchall()
	rowList = []
	for issue in issues:
		rowdict = {'title':issue[0],'description':issue[1]}
		rowList.append(rowdict)
	return rowList
	

def updateIssue(title,description,image,issue_id):
	cursor = connection.cursor()
	cursor.execute("update issue set title= %s, description=%s, image = %s where id = %s",[title,description,image,issue_id])
	connection.commit()
	return cursor.execute



