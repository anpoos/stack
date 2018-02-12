from unittest import TestCase
from django.db import connection

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
		expected = {'id':2L,
					'first_name':u'anbu',
					'last_name':u'b',
					'emp_no':u'107',
					'user_name':u'anbu',
					'email':u'anbu@gmail.com',
					'is_active':u'1'
					}
		self.assertEqual(authenticate,expected)

		#correct username password for inactive user
		authenticate = service.authenticate('saran','saran')
		self.assertEqual(authenticate,False)

	def test_createIssue(self):
		issue1 = service.createIssue('title 1','description 1', 1)
		self.assertEqual(issue1,1)
		issue1 = service.createIssue('','', 1)