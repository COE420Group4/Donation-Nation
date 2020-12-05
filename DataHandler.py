# Import our database and initialize it
from db import DB
import send_email
import re
import hashlib
import uuid
import traceback
from datetime import datetime
from base64 import standard_b64encode


sql = DB()
sql.clear_db()
sql.init_db()
sql.populate()

# Checker function to check all form variables
def check_form(form, paramters):
	for param in paramters:
		if form[param] and len(form[param]) < 1:
			return False
	return True

# Checker function to check that all form variables are alphabetic
def is_all_alpha(form, paramters):
	for param in paramters:
		if not all(x.isalpha() or x.isspace() for x in form[param]):
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
	regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if re.search(regex, form[parameter]):
		pass
	else:
		raise UserException(f'{parameter.capitalize()} must be a valid email.')

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in {'jpg','png','jpeg'}

class User:
	def insert(form):
		# Check that all information is here
		if check_form(form, ['firstName', 'lastName', 'dob', 'city', 'emirate', 'POBox', 'address1', 'address2', 'phone', 'email', 'password', 'confirmPassword']):
			is_all_alpha(form, ['firstName', 'lastName', 'city', 'emirate'])
			is_all_alnum(form, ['POBox'])
			is_all_numeric(form, ['phone'])
			is_email(form, 'email')
			User.check_phone_exists(form['phone'])
			User.check_email_exists(form['email'])
			hash = ''
			if form['password'] != form['confirmPassword']:
				raise UserException('Both password fields must be the same.')
			else:
				hash = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
				user_uuid = str(uuid.uuid4())
			try:
				dbcon = sql.connect()
				dbcon.execute("INSERT INTO users (UUID, first_name, last_name, dob, city, emirate, po_box, address_1, address_2, phone, email, password, isAdmin, isVerified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,0,0)", (user_uuid,form['firstName'], form['lastName'], form['dob'], form['city'], form['emirate'], form['POBox'], form['address1'], form['address2'], form['phone'], form['email'], hash))
				verification_uuid = str(uuid.uuid4())
				dbcon.execute("INSERT INTO verifications VALUES (?,?)", (user_uuid, verification_uuid))

				# Send email to user for verification
				send_email.send('Email Verification', f'Hi {form["firstName"].strip()}!\n\n\nThank you for signing up for DonationNation!\n\nTo complete your registration and enable your account, please verify your email by visiting the link: http://127.0.0.1:5000/verify_user/{verification_uuid}\n\nRegards,\nDonationNation', [form['email'],])

				# Commit changes and close the db connection
				dbcon.commit()
				dbcon.close()
			except Exception:
				traceback.print_exc()
				raise UserException("Something went wrong. Contact an admin.")
		else:
			raise UserException("Invalid or missing information!")

	def check_phone_exists(value):
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT id FROM users WHERE phone=?", (value,))
			if cur.fetchone() is not None:
				cur.close()
				dbcon.close()
				raise UserException("A user with that phone number already exists.")
			else:
				cur.close()
				dbcon.close()
		except UserException as e:
			raise e
		except Exception:
			traceback.print_exc()
			raise UserException("Something went wrong. Contact an admin.")

	def check_email_exists(value):
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT id FROM users WHERE email=?", (value,))
			if cur.fetchone() is not None:
				cur.close()
				dbcon.close()
				raise UserException("A user with that email already exists.")
			else:
				cur.close()
				dbcon.close()
		except UserException as e:
			raise e
		except Exception:
			traceback.print_exc()
			raise UserException("Something went wrong. Contact an admin.")

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
		except Exception:
			traceback.print_exc()
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
					if data[14] == 0:
						raise UserException("You haven't verified your email yet! Please verify it then try again.")
					return data
				else:
					raise UserException("Invalid email or password. Please try again.")
			except UserException as e:
				raise e
			except Exception:
				traceback.print_exc()
				raise UserException("Something went wrong. Contact an admin.")
		else:
			raise UserException("Invalid or missing information!")

	def verify(verify_uuid):
		try:
			# Check that the verification UUID exists
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT user_uuid FROM verifications WHERE verification_uuid=?", (verify_uuid,))
			uuid = cur.fetchone()
			if uuid is None:
				raise UserException("NotFound") # Generic name so that we can catch it in flask

			# If we're here, then the verification exists and we should verify the user
			cur.execute("UPDATE users SET isVerified=1 WHERE UUID=?", (uuid[0],))

			# Remove the verification from the database
			cur.execute("DELETE FROM verifications WHERE user_uuid=?", (uuid[0],))

			# Commit the changes and close connections
			dbcon.commit()
			cur.close()
			dbcon.close()
		except UserException as e:
			raise e
		except Exception as e:
			# We raise any exception so that the flask app can handle it
			traceback.print_exc()
			raise e

	def addItem(form,session,files):
		if check_form(form, ['name','category','condition','description','organization','time']) and (files['image'] is not None):
			item_uuid = str(uuid.uuid4())
			user_uuid = session['isLoggedIn'][1]
			current_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
			image = standard_b64encode(files['image'].read())
			try:
				org = Organization.fetchByUUID(form['organization'])
				send_email.send('New Item Offered!', f'Hi {org[2].strip()}!\n\n\nYou have been offered a new item ({form["name"]}) [{form["category"]}]! Log into the application and to approve or reject this item!\n\nRegards,\nDonationNation', [org[12],])
				dbcon = sql.connect()
				cur = dbcon.cursor()
				cur.execute("INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,0)",(item_uuid,form['name'],form['category'],form['condition'],form['description'],form['organization'],user_uuid,current_time,form['time'],image))
				dbcon.commit()
				cur.close()
				dbcon.close()
			except Exception as e:
				# We raise any exception so that the flask app can handle it
				traceback.print_exc()
				raise e

	def removeItem(uuid):
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute('DELETE FROM items WHERE UUID=?', (uuid,))
			dbcon.commit()
			cur.close()
			dbcon.close()
		except UserException as ue:
			raise ue
		except Exception:
			traceback.print_exc()
			raise UserException('An issue has occurred. Please contact an admin.')

	def getAllItems(user_uuid):
		# Connect to the database
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT items.id, items.UUID, item_name, category, condition, description, org_id, user_id, time_submitted, pickup_time, image, items.status, organizations.name FROM items, organizations WHERE organizations.UUID=items.org_id AND user_id=?", (user_uuid,))
			items = cur.fetchall()
			cur.close()
			dbcon.close()
			if len(items) > 0:
				return items
			else:
				raise UserException("No items exist for this user.")
		except UserException as ue:
			raise ue
		except Exception as e:
			raise UserException("Something went wrong. Please contact an admin.")

	def changePassword(form, session):
		if check_form(form, ['password', 'confirmPassword']):
			hash = ''
			if form['password'] != form['confirmPassword']:
				raise UserException('Both password fields must be the same.')
			else:
				hash = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
				try:
					dbcon = sql.connect()
					dbcon.execute("UPDATE users set password = ? where UUID = ?", (hash, session['isLoggedIn'][1]))

					# Commit changes and close the db connection
					dbcon.commit()
					dbcon.close()
				except Exception:
					traceback.print_exc()
					raise UserException("Something went wrong. Contact an admin.")
		else:
			raise UserException("Invalid or missing information!")


	def editInformation(form, session):
		# Check that all information is here
		if check_form(form, ['city', 'emirate', 'POBox', 'address1', 'address2', 'phone']):
			is_all_alpha(form, ['city', 'emirate'])
			is_all_alnum(form, ['POBox'])
			is_all_numeric(form, ['phone'])
			try:
				dbcon = sql.connect()
				cur = dbcon.cursor()
				cur.execute("UPDATE users SET city = ?, emirate = ?, po_box = ?, address_1 = ?, address_2 = ?, phone = ? WHERE UUID = ?", (form['city'], form['emirate'], form['POBox'], form['address1'], form['address2'], form['phone'], session['isLoggedIn'][1]))
				dbcon.commit()
				cur.execute("SELECT * FROM users WHERE UUID=?", (session['isLoggedIn'][1],))
				data = cur.fetchone()
				cur.close()
				dbcon.close()
				return data
			except Exception:
				traceback.print_exc()
				raise UserException("Something went wrong. Contact an admin.")
class UserException(Exception):
	def __init__(self, message):
		self.reason = message
		super().__init__(self, self.reason)

class Organization:
	def insert(form, files):
		if check_form(form, ['name', 'registrationNumber', 'city', 'emirate', 'POBox', 'address1', 'address2', 'phone', 'email', 'password', 'confirmPassword']) and (files['logo'] is not None):
			is_all_alpha(form, ['name', 'city', 'emirate'])
			is_all_alnum(form, ['POBox'])
			is_all_numeric(form, ['phone', 'registrationNumber'])
			is_email(form, 'email')
			Organization.check_phone_exists(form['phone'])
			Organization.check_email_exists(form['email'])
			hash = ''
			logo = standard_b64encode(files['logo'].read())
			if form['password'] != form['confirmPassword']:
				raise OrgException('Both password fields must be the same.')
			else:
				hash = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
				org_uuid = str(uuid.uuid4())
			try:
				dbcon = sql.connect()
				dbcon.execute("INSERT INTO organizations (UUID, name, status, license_no, city, emirate, po_box, address_1, address_2, phone, logo, email, password) VALUES (?,?,0,?,?,?,?,?,?,?,?,?,?)", (org_uuid, form['name'], form['registrationNumber'], form['city'], form['emirate'], form['POBox'], form['address1'], form['address2'], form['phone'], logo, form['email'], hash))
				verification_uuid = str(uuid.uuid4())
				dbcon.execute("INSERT INTO verifications VALUES (?,?)", (org_uuid, verification_uuid))

				# Send email to user for verification
				send_email.send('Email Verification', f'Hi {form["name"].strip()}!\n\n\nThank you for signing up for DonationNation!\n\nTo complete your registration and enable your account, please verify your email by visiting the link: http://127.0.0.1:5000/verify_org/{verification_uuid}\n\nRegards,\nDonationNation', [form['email'],])

				# Commit changes and close the db connection
				dbcon.commit()
				dbcon.close()
			except Exception:
				traceback.print_exc()
				raise OrgException("Something went wrong. Contact an admin.")
		else:
			raise OrgException("Invalid or missing information!")

	def check_phone_exists(value):
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT id FROM organizations WHERE phone=?", (value,))
			if cur.fetchone() is not None:
				cur.close()
				dbcon.close()
				raise OrgException("An organization with that phone number already exists.")
			else:
				cur.close()
				dbcon.close()
		except OrgException as e:
			raise e
		except Exception:
			traceback.print_exc()
			raise OrgException("Something went wrong. Contact an admin.")

	def check_email_exists(value):
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT id FROM organizations WHERE email=?", (value,))
			if cur.fetchone() is not None:
				cur.close()
				dbcon.close()
				raise OrgException("An organization with that email already exists.")
			else:
				cur.close()
				dbcon.close()
		except OrgException as e:
			raise e
		except Exception:
			traceback.print_exc()
			raise OrgException("Something went wrong. Contact an admin.")

	def login(form):
		try:
			if check_form(form, ['email', 'password']):
				hash = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()

				# Verify the creds
				dbcon = sql.connect()
				cur = dbcon.cursor()
				cur.execute("SELECT id,UUID,name,status,license_no,city,emirate,po_box,address_1,address_2,phone,1,email,password FROM organizations WHERE email=? AND password=?", (form['email'], hash))
				org_data = cur.fetchone()
				if org_data is not None:
					# Check that the user is verified
					if org_data[3] == 2:
						# This means the credentials are correct and we do nothing
						return org_data
					elif org_data[3] == 1:
						raise OrgException("An administrator has not verified your account yet. Please wait and try later.")
					else:
						raise OrgException("Please verify your email so that an admin can review your account.")
				else:
					raise OrgException("Invalid email or password.")
			else:
				raise OrgException("Missing or invalid information!")
		except OrgException as e:
			raise e
		except Exception:
			traceback.print_exc()
			raise OrgException("Something went wrong. Contact an admin.")

	def verify(verify_uuid):
		try:
			# Check if this verification_uuid exists
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT user_uuid FROM verifications WHERE verification_uuid=?", (verify_uuid,))
			uuid = cur.fetchone()
			if uuid is None:
				raise OrgException("NotFound") # Generic name so that we can catch it in flask

			# If we're here, then the verification exists and we should verify the org
			cur.execute("UPDATE organizations SET status=1 WHERE UUID=?", (uuid[0],))

			# Remove the verification from the database
			cur.execute("DELETE FROM verifications WHERE user_uuid=?", (uuid[0],))

			# Commit the changes and close connections
			dbcon.commit()
			cur.close()
			dbcon.close()
		except OrgException as e:
			raise e
		except Exception:
			traceback.print_exc()
			raise OrgException("Something went wrong. Contact an admin.")

	def accept(org_uuid):
		try:
			org_data = Organization.fetchByUUID(org_uuid)

			# Check their status
			if org_data[3] == 2:
				raise OrgException("Organization already accepted!")
			else:
				send_email.send('Application Accepted', f'Hi {org_data[2].strip()}!\n\n\nWe are pleased to inform you that your application ({org_data[1]}) for being an organization registered with us has been accepted. You can now log in to the application and begin accepting donations.\n\nRegards,\nDonationNation', [org_data[12],])
				dbcon = sql.connect()
				cur = dbcon.cursor()
				cur.execute("UPDATE organizations SET status=2 WHERE UUID=?", (org_data[1],))
				cur.close()
				dbcon.commit()
				dbcon.close()
		except OrgException as e:
			raise e
		except Exception as e:
			traceback.print_exc()
			raise e

	def reject(org_uuid):
		try:
			org_data = Organization.fetchByUUID(org_uuid)
			print(org_data)
			# Check their status
			if org_data[3] == 2:
				raise OrgException("Organization already accepted!")
			else:
				send_email.send('Application Rejected', f'Hi {org_data[2].strip()}!\n\n\nWe regret to inform you that your application ({org_data[1]}) for being an organization registered with us has been rejected. You can contact us at tips@fbi.gov to repeal your rejection.\n\nRegards,\nDonationNation', [org_data[12],])
				dbcon = sql.connect()
				cur = dbcon.cursor()
				cur.execute("DELETE FROM organizations WHERE UUID=?", (org_data[1],))
				cur.fetchone()
				cur.close()
				dbcon.commit()
				dbcon.close()
		except OrgException as e:
			raise e
		except Exception as e:
			traceback.print_exc()
			raise e

	def getAll():
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT * FROM organizations")
			data = cur.fetchall()
			cur.close()
			dbcon.close()
			if data is not None:
				return data
			else:
				raise OrgException("There are no organizations registered yet.")
		except Exception as e:
			raise e

	def fetchByUUID(org_uuid):
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT * FROM organizations WHERE UUID=?", (org_uuid,))
			data = cur.fetchone()
			cur.close()
			dbcon.close()
			if data is not None:
				return data
			else:
				return False
		except Exception as e:
			return False

	def getAllItems(org_uuid):
		# Connect to the database
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT * FROM items WHERE org_id=?", (org_uuid))
			items = cur.fetchall()
			cur.close()
			dbcon.close()
			if items is not None:
				return items
			else:
				raise OrgException("No items exist for this organization.")
		except Exception as e:
			raise e

	def getAllVerified():
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT * FROM organizations WHERE status=2")
			data = cur.fetchall()
			cur.close()
			dbcon.close()
			if data is not None:
				return data
			else:
				raise OrgException("There are no organizations registered yet.")
		except Exception as e:
			raise e

	def getAllPending():
		try:
			dbcon = sql.connect()
			cur = dbcon.cursor()
			cur.execute("SELECT * FROM organizations WHERE status!=2")
			data = cur.fetchall()
			cur.close()
			dbcon.close()
			if data is not None:
				return data
			else:
				raise OrgException("There are no organizations registered yet.")
		except Exception as e:
			raise e

	def changePassword(form, session):
		if check_form(form, ['password', 'confirmPassword']):
			hash = ''
			if form['password'] != form['confirmPassword']:
				raise OrgException('Both password fields must be the same.')
			else:
				hash = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
				user_uuid = str(uuid.uuid4())
				try:
					dbcon = sql.connect()
					dbcon.execute("UPDATE organizations set password = ? where UUID = ?", (hash, session['isLoggedIn'][1]))

					# Commit changes and close the db connection
					dbcon.commit()
					dbcon.close()
				except Exception:
					traceback.print_exc()
					raise OrgException("Something went wrong. Contact an admin.")
		else:
			raise OrgException("Invalid or missing information!")

class OrgException(Exception):
	def __init__(self, message):
		self.reason = message
		super().__init__(self, self.reason)