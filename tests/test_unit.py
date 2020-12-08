import pytest
import hashlib
from uuid import uuid4
from datetime import datetime
import sys
sys.path.append('.')
from DataHandler import *
from db import DB
sql = DB()

def test_initDB():
	# Let's reset the DB before we start
	sql.clear_db()
	sql.init_db()
	sql.populate()

def test_registerUser():
	# Test with missing form data
	form = {}
	with pytest.raises(UserException):
		User.insert(form)

	# Test with empty form parameters
	form = {}
	form['firstName'] = ''
	form['lastName'] = ''
	with pytest.raises(UserException):
		User.insert(form)

	# Test with data where passwords aren't the same
	# 'firstName', 'lastName', 'dob', 'city', 'emirate', 'POBox', 'address1', 'address2', 'phone', 'email', 'password', 'confirmPassword'
	form = {}
	form['firstName'] = 'John'
	form['lastName'] = 'Doe'
	form['dob'] = ''
	form['city'] = 'Sharjah'
	form['emirate'] = 'Sharjah'
	form['POBox'] = '12345'
	form['address1'] = 'Somewhere'
	form['address2'] = 'Someplace'
	form['phone'] = '0505656231'
	form['email'] = 'john@email.com'
	form['password'] = hashlib.sha256(b'password').hexdigest()
	form['confirmPassword'] = ''
	with pytest.raises(UserException):
		User.insert(form)

	# Fix the password and submit with complete information
	form['confirmPassword'] = hashlib.sha256(b'password').hexdigest()
	User.insert(form)

	# Test that the user was inserted
	dbcon = sql.connect()
	cur = dbcon.cursor()
	data = cur.execute('SELECT * FROM users WHERE phone=?', ('0505656231',)).fetchone()
	assert data is not None
	assert len(data) > 0
	assert data[2] == 'John'
	cur.close()
	dbcon.close()

def test_registerOrganization():
	# Test with missing form data
	form = {}
	files = {}
	with pytest.raises(OrgException):
		Organization.insert(form, files)

	# Test with empty form parameters
	form = {}
	files = {}
	files['image'] = open('./assets/dubaiCares.jpg', 'rb')
	form['name'] = ''
	with pytest.raises(OrgException):
		Organization.insert(form, files)

	# Test with valid data except the passwords mismatch
	# 'name', 'registrationNumber', 'city', 'emirate', 'POBox', 'address1', 'address2', 'phone', 'email', 'password', 'confirmPassword'
	form = {}
	files = {}
	files['logo'] = open('./assets/dubaiCares.jpg', 'rb')
	form['name'] = 'Good Will'
	form['registrationNumber'] = '8883434888'
	form['city'] = 'Sharjah'
	form['emirate'] = 'Sharjah'
	form['POBox'] = '12345'
	form['address1'] = 'Somewhere'
	form['address2'] = 'Someplace'
	form['phone'] = '0509876123'
	form['email'] = 'contact@goodwill.org'
	form['password'] = hashlib.sha256(b'password').hexdigest()
	form['confirmPassword'] = ''
	with pytest.raises(OrgException):
		Organization.insert(form, files)

	# Fix the password and resubmit
	form['confirmPassword'] = hashlib.sha256(b'password').hexdigest()
	Organization.insert(form, files)

	# Test that the org was inserted
	dbcon = sql.connect()
	cur = dbcon.cursor()
	data = cur.execute('SELECT * FROM organizations WHERE phone=?', ('0509876123',)).fetchone()
	assert data is not None
	assert len(data) > 0
	assert data[2] == 'Good Will'
	cur.close()
	dbcon.close()

def test_addItem():
	pass

def test_getAllItemsOrg():
	dbcon = sql.connect()
	cur = dbcon.cursor()
	red_uuid = cur.execute('SELECT UUID FROM organizations WHERE email="contact@redcrescent.org"').fetchone()[0]
	cur.close()
	dbcon.close()
	assert red_uuid is not None

	# Testing with non existent org
	with pytest.raises(OrgException):
		Organization.getAllItems('')

	# Testing with an existing org
	items = Organization.getAllItems(red_uuid)
	assert items is not None
	assert len(items) > 0
	for item in items:
		assert len(item) == 14

def test_getAllItemsUser():
	dbcon = sql.connect()
	cur = dbcon.cursor()
	donald_uuid = cur.execute('SELECT UUID FROM users WHERE first_name="Donald"').fetchone()[0]
	cur.close()
	dbcon.close()
	assert donald_uuid is not None

	# Testing with a non existent user
	with pytest.raises(UserException):
		User.getAllItems('')

	# Testing with an existing user
	items = User.getAllItems(donald_uuid)
	assert items is not None
	assert len(items) > 0
	for item in items:
		assert len(item) == 13

def test_getAllOrgs():
	orgs = Organization.getAll()
	assert orgs is not None
	assert len(orgs) > 0
	for org in orgs:
		assert len(org) == 14

def test_fetchOrgByUUID():
	dbcon = sql.connect()
	cur = dbcon.cursor()
	red_uuid = cur.execute('SELECT UUID FROM organizations WHERE email="contact@redcrescent.org"').fetchone()[0]
	cur.close()
	dbcon.close()

	# Non existing org
	assert Organization.fetchByUUID('') is False

	# Existing org, Red Crescent
	fetched_data = Organization.fetchByUUID(red_uuid)
	assert fetched_data is not None
	assert len(fetched_data) > 0
	assert fetched_data[1] == red_uuid
	assert fetched_data[2] == 'Red Crescent'

def test_fetchUserByUUID():
	dbcon = sql.connect()
	cur = dbcon.cursor()
	donald_uuid = cur.execute('SELECT UUID FROM users WHERE first_name="Donald"').fetchone()[0]
	cur.close()
	dbcon.close()

	# Non existing user
	assert User.fetchByUUID('') is False

	# Existing user, donald
	fetched_data = User.fetchByUUID(donald_uuid)
	assert fetched_data is not None
	assert len(fetched_data) > 0
	assert fetched_data[1] == donald_uuid
	assert fetched_data[2] == 'Donald'

def test_orgExists():
	pass

def test_userExists():
	pass

# ? Optional
def test_is_all_alpha():
	pass

def test_is_all_alnum():
	pass

def test_is_all_numeric():
	pass

def test_is_email():
	pass
