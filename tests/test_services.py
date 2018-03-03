from unittest import TestCase
from django.db import connection
import datetime

#from django.test import TestCase
from stack import service
class TestLogin(TestCase):

	def setUp(self):
		
		f = open('migration/sql_query.sql', 'r')
		query = " ".join(f.readlines())
		cursor = connection.cursor()
		cursor.execute(query)

	def tearDown(self):
		
		cursor = connection.cursor()
		cursor.execute('drop table employee')
		cursor.execute('drop table issue')
		cursor.execute('drop table solution')
		connection.close()

	def test_authenticate(self):
		
		# wrong user name passowrd
		authenticate = service.authenticate('test_user','test_password')
		self.assertEqual(authenticate,False)

		# correct user and password
		authenticate = service.authenticate('anbu','anbu')
		expected = {
					'first_name':u'anbu',
					'last_name':u'b',
					'emp_no':u'101',
					'user_name':u'anbu',
					'email':u'anpoo.star@gmail.com',
					'is_active':u'1'
					}
		self.assertEqual(authenticate,expected)

		#correct username password for inactive user
		authenticate = service.authenticate('anbu','anbu1')
		self.assertEqual(authenticate,False)

	def test_createIssue(self):
		issue1 = service.createIssue('title 1','description 1','image 1', 1)
		self.assertEqual(issue1,1)
		issue1 = service.createIssue('','','', 1)
		self.assertEqual(issue1,1)

	def test_getIssues(self):
		issue1 = service.createIssue('title 1','description 1','image 1', 1)
		issue2 = service.getIssues(0,3)
		numOfRecords = len(issue2)
		self.assertEqual(numOfRecords,1)


	def test_totalRecord(self):
		issue1 = service.createIssue('title 1','description 1','image 1', 1)

		record = service.totalRecord()
		self.assertEqual(record,1)
	
	def test_getIssueById(self):
		issue1 = service.createIssue('test','test case','image', 1)

		rowdict = service.getIssueById(1)
		expected = {'id':1L,
					'first_name':u'saranya',
					'last_name':u'A',
					'title':u'test',
					'description':u'test case',
					'image':u'image',
					'created_date':datetime.datetime.now().date(),
					}
		self.assertEqual(rowdict,expected)

		# rowdict = service.getIssueById(10)
		# self.assertEqual(rowdict,False)

	def test_createSolution(self):
		solution = service.createSolution('example..','image',1,1)
		self.assertEqual(solution,1)

	def test_getEmailsOfAll(self):

		mailid = service.getEmailsOfAll()
		mailid1 = {'mail_id':u'aa@gmail.com'}
		# mailid = len(mailid)
		self.assertEqual(mailid,mailid1)

	def test_getUserById(self):
		user_name = service.getUserById('1')
		user_name = len(user_name)
		self.assertEqual(user_name,2)

	def test_getSolutionsForIssue(self):
		solution = service.createSolution('example..','image',1,1)

		ans = service.getSolutionsForIssue(1)
		ans = len(ans)
		self.assertEqual(ans,1)

	def test_getSearchResult(self):
		issue1 = service.createIssue('test case','example description ','image', 1)

		result = service.getSearchResult('case',0,3)
		self.assertEqual(result[1],1)

		result = service.getSearchResult('example',0,3)
		self.assertEqual(result[1],1)

		result = service.getSearchResult('non exist',0,3)
		self.assertEqual(result[1],0)		

	def test_getKeyword(self):
		key= service.getKeyword('what is test method')
		print key