# Import our database and initialize it
from db import DB
import re
import hashlib
import uuid

sql = DB()
sql.init_db()

# Checker function to check all form variables
# check_form(form, ['email', 'password'])
def check_form(form, paramters):
	for param in paramters:
		if form[param] and len(form[param]) < 1:
			return False
	return True

# Checker function to check that all form variables are alphabetic
def is_all_alpha(form, paramters):
	for param in paramters:
		if not form[param].isalpha():
			raise UserException(f'{param.capitalize()} must consist of only alphabetic characters.')
	return True

# Checker function to check that all form variables are alphanum
def is_all_alnum(form, paramters):
	for param in paramters:
		if not form[param].isalnum():
			raise UserException(f'{param.capitalize()} must consist of only alphanumeric characters.')
	return

# Checker function to check that all form variables are alphanum
def is_all_numeric(form, paramters):
	for param in paramters:
		if not form[param].isnumeric():
			raise UserException(f'{param.capitalize()} must consist of only numeric characters.')
	return True

def is_email(form, parameter):
	regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if re.search(regex, form[parameter]):
		pass
	else:
		raise UserException(f'{parameter.capitalize()} must be a valid email.')

class User:
	def insert(form):
		# Check that all information is here
		if check_form(form, ['firstName', 'lastName', 'dob', 'city', 'emirate', 'POBox', 'address1', 'address2', 'phone', 'email', 'password', 'confirmPassword']):
			is_all_alpha(form, ['firstName', 'lastName', 'city', 'emirate'])
			is_all_alnum(form, ['POBox'])
			is_all_numeric(form, ['phone'])
			is_email(form, 'email')
			hash = ''
			if form['password'] != form['confirmPassword']:
				raise UserException('Both password fields must be the same.')
			else:
				hash = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
				user_uuid = str(uuid.uuid4())
			try:
				dbcon = sql.connect()
				dbcon.execute("INSERT INTO users (UUID, first_name, last_name, dob, city, emirate, po_box, address_1, address_2, phone, email, password, isAdmin) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,0)", (user_uuid,form['firstName'], form['lastName'], form['dob'], form['city'], form['emirate'], form['POBox'], form['address1'], form['address2'], form['phone'], form['email'], hash))
				dbcon.commit()
				dbcon.close()
			except Exception as e:
				print(e)
				raise UserException("Something went wrong. Contact an admin.")
		else:
			raise UserException("Invalid or missing information!")

	# TODO: later
	def check_phone_exists(value):
		try:
			dbcon = sql.connect()
			dbcon.execute("SELECT id FROM users WHERE phone=?", (value))
			dbcon.close()
		except Exception as e:
			pass

	# Get user information by supplying their UUID
	def fetchByUUID(user_uuid):
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT * FROM users WHERE UUID=?", (user_uuid,))
			res = cur.fetchone()
			cur.close()
			dbcon.close()
			if res is not None:
				return res
			else:
				return False
		except Exception as e:
			print(e)
			return False

	def login(form):
		if check_form(form, ['email', 'password']):
			hash = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
			try:
				dbcon = sql.connect()
				cur = dbcon.cursor()
				cur.execute("SELECT * FROM users WHERE email=? AND password=?", (form['email'], hash))
				data = cur.fetchone()
				if data is not None:
					return data
				else:
					raise UserException("Invalid email or password. Please try again.")
			except UserException as e:
				raise e
			except Exception as e:
				print(e)
				raise UserException("Something went wrong. Contact an admin.")

class UserException(Exception):
	def __init__(self, message):
		self.reason = message
		super().__init__(self, self.reason)