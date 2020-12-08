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

# TODO: do this.
def test_addItem():
	# Empty form
	# Missing image
	# Nonexistent user uuid
	# Nonexistend org uuid
	# All good
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
	# Existing email, should raise
	with pytest.raises(OrgException):
		Organization.check_email_exists('contact@redcrescent.org')

	# Non existing email, should run fine
	Organization.check_email_exists('doestnot@exist.org')

	# Existing phone number, should raise
	with pytest.raises(OrgException):
		Organization.check_phone_exists('062224444')

	# Non existing phone number, should run fine
	Organization.check_phone_exists('022222222')

def test_userExists():
	# Existing email, should raise
	with pytest.raises(UserException):
		User.check_email_exists('donald@email.com')

	# Non existing email, should run fine
	User.check_email_exists('doestnot@exist.org')

	# Existing phone number, should raise
	with pytest.raises(UserException):
		User.check_phone_exists('0508764563')

	# Non existing phone number, should run fine
	User.check_phone_exists('0502222222')

def test_is_all_alpha():
	form = {}

	# Valid input, no exception
	form['test'] = ''
	is_all_alpha(form, ['test'])
	form['test'] = 'a     b'
	is_all_alpha(form, ['test'])
	form['test'] = 'helloTEST'
	is_all_alpha(form, ['test'])

	# Invalid input, exception
	form['test'] = '<>#'
	with pytest.raises(UserException):
		is_all_alpha(form, ['test'])
	form['test'] = '12123123'
	with pytest.raises(UserException):
		is_all_alpha(form, ['test'])
	form['test'] = 'hello Gamer1'
	with pytest.raises(UserException):
		is_all_alpha(form, ['test'])

def test_is_all_alnum():
	form = {}

	# Valid input, no exception
	form['test'] = 'helloTEST'
	is_all_alnum(form, ['test'])
	form['test'] = '12123123'
	is_all_alnum(form, ['test'])
	form['test'] = 'Gamer1'
	is_all_alnum(form, ['test'])

	# Invalid input, exception
	form['test'] = '<>#'
	with pytest.raises(UserException):
		is_all_alnum(form, ['test'])
	form['test'] = ''
	with pytest.raises(UserException):
		is_all_alnum(form, ['test'])
	form['test'] = 'a     b'
	with pytest.raises(UserException):
		is_all_alnum(form, ['test'])

def test_is_all_numeric():
	form = {}

	# Valid input, no exception
	form['test'] = '12123123'
	is_all_numeric(form, ['test'])

	# Invalid input, exception
	form['test'] = 'one'
	with pytest.raises(UserException):
		is_all_numeric(form, ['test'])
	form['test'] = ''
	with pytest.raises(UserException):
		is_all_numeric(form, ['test'])

def test_is_email():
	form = {}

	# Valid email, all good
	form['test'] = 'testing@test.com'
	is_email(form, 'test')

	# Invalid email, exception
	form['test'] = ''
	with pytest.raises(UserException):
		is_email(form, 'test')
	form['test'] = 'invalid'
	with pytest.raises(UserException):
		is_email(form, 'test')
	form['test'] = 'notquite@yes'
	with pytest.raises(UserException):
		is_email(form, 'test')