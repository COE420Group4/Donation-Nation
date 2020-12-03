# DataHandler
from DataHandler import OrgException, Organization, User, UserException

# Library imports
import os
from flask import Flask, session, render_template, request, abort, redirect, flash, url_for
app = Flask(__name__, static_url_path='/assets', static_folder='assets')
app.secret_key = os.urandom(64)

# Flask routes
@app.route('/', methods=['GET'])
def main():
	return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if not 'isLoggedIn' in session:
		if request.method == 'POST':
			if request.form.get('type') == 'user':
				try:
					data = User.login(request.form)
					session['isLoggedIn'] = data
					session['type'] = 'user'
					return redirect('/dashboard')
				except UserException as ue:
					flash(ue.reason, 'error')
					return redirect('/login?type=user')
			elif request.form.get('type') == 'org':
				try:
					data = Organization.login(request.form)
					session['isLoggedIn'] = data
					session['type'] = 'org'
					return redirect('/dashboard')
				except OrgException as ue:
					flash(ue.reason, 'error')
					return redirect('/login?type=org')
			else:
				abort(400)
		else:
			return render_template('login.html', type=request.args.get('type'))
	else:
		return 'Success'

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('isLoggedIn', None)
	session.pop('type', None)
	flash('You were logged out successfully.','success')
	return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if request.form.get('type') == 'user':
			try:
				User.insert(request.form)
				flash('You have successfully registered. Please click the link in your email to verify your account and get access.', 'success')
				return redirect('/login?type=user')
			except UserException as ue:
				flash(ue.reason, 'error')
				return redirect('/register?type=user')
		elif request.form.get('type') == 'org':
			try:
				data = Organization.insert(request.form, request.files)
				flash('You have successfully registered. Please click the link in your email to verify your account and get access.', 'success')
				return redirect('/login?type=org')
			except OrgException as ue:
				flash(ue.reason, 'error')
				return redirect('/register?type=org')
		else:
			abort(400)
	else:
		return render_template('register.html', type=request.args.get('type'))

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html', userData=session['isLoggedIn'])

@app.route('/orgs', methods=['GET'])
def orgs():
	try:
		orgs = Organization.getAllVerified()
		return render_template('orgs.html', orgData=orgs)
	except OrgException as ue:
		flash(ue.reason, 'error')
		return redirect('/')


@app.route('/items', methods=['GET', 'POST'])
def items():
	if 'isLoggedIn' in session:
		if session['type'] == 'user':
			try:
				items = User.getAllItems(session['isLoggedIn'][1])
				return render_template('itemsUser.html', items_list=items)
			except UserException as ue:
				flash(ue.reason, 'error')
				# WHERE DO I REDIRECT IF THE USER HAS NO ITEMS. SHOUlD BE THE SAME PAGE RIGHT?
				return redirect('/addItem')
		else:
			try:
				items = Organization.getAllItems(session['isLoggedIn'][1])
				return render_template('itemsOrg.html', items_list=items)
			except UserException as ue:
				flash(ue.reason, 'error')
				# WHERE DO I REDIRECT IF THE USER HAS NO ITEMS. SHOUlD BE THE SAME PAGE RIGHT?
				return redirect('/addItem')

@app.route('/admin', methods=['GET'])
def admin():
	if 'isLoggedIn' in session:
		if session['type'] == 'user' and session['isLoggedIn'][13] == 1:
			try:
				orgs = Organization.getAll()
				return render_template('admin.html', orgData=orgs)
			except OrgException as oe:
				flash(oe.reason, 'error')
				return redirect('/dashboard')
		else:
			flash('You are not authorized to be here!', 'error')
			return redirect('/login?type=user')
	else:
		flash('You are not logged in yet! Please login then try again', 'error')
		return redirect('/login?type=user')

@app.route('/admin/reject/<uuid>', methods=['GET'])
def reject_org(uuid):
	if 'isLoggedIn' in session:
		if session['type'] == 'user' and session['isLoggedIn'][13] == 1:
			try:
				Organization.reject(uuid)
				flash('Successfully rejected the organization.', 'success')
				return redirect('/admin')
			except OrgException as oe:
				flash(oe.reason, 'error')
				return redirect('/admin')
		else:
			flash('You are not authorized to be here!', 'error')
			return redirect('/login?type=user')
	else:
		flash('You are not logged in yet! Please login then try again', 'error')
		return redirect('/login?type=user')

@app.route('/admin/approve/<uuid>', methods=['GET'])
def approve_org(uuid):
	if 'isLoggedIn' in session:
		if session['type'] == 'user' and session['isLoggedIn'][13] == 1:
			try:
				Organization.accept(uuid)
				flash('Successfully approved the organization.', 'success')
				return redirect('/admin')
			except OrgException as oe:
				flash(oe.reason, 'error')
				return redirect('/admin')
		else:
			flash('You are not authorized to be here!', 'error')
			return redirect('/login?type=user')
	else:
		flash('You are not logged in yet! Please login then try again', 'error')
		return redirect('/login?type=user')

@app.route('/addItem', methods=['GET', 'POST'])
def donate():
	if request.method == 'POST':
		try:
			User.addItem(request.form, session)
			return 'Success'
		except UserException as ue:
			flash(ue.reason, 'error')
			return redirect('/addItem')
	else:
		print(Organization.getAllVerified())
		return render_template('addItem.html', orgs_details=Organization.getAllVerified())

@app.route('/orgProfile', methods=['GET'])
def orgProfile():
	return render_template('orgProfile.html')

@app.route('/userProfile', methods=['GET'])
def userProfile():
	if 'isLoggedIn' in session and session['type'] == 'user':
		return render_template('userProfile.html', userData=session['isLoggedIn'])
	else:
		flash('You are not logged in yet! Please login then try again', 'error')
		return redirect('/login?type=user')

# The user information page from organization's perspective
# * This is an example of how we pass variables in the URL path
@app.route('/user/<uuid>', methods=['GET'])
def viewUser(uuid):
	if session['type'] == 'org':
		# Fetch user info
		user_info = User.fetchByUUID(uuid)
		if user_info is not False:
			return render_template('viewUser.html', userData=user_info)
		else:
			abort(404)
	else:
		abort(404)

@app.route('/org/<uuid>', methods=['GET'])
def viewOrg(uuid):
	# Fetch user info
	org_data = Organization.fetchByUUID(uuid)
	if org_data is not False:
		return render_template('viewOrg.html', orgData=org_data)
	else:
		abort(404)

# Verifying users' emails
@app.route('/verify_user/<verify_uuid>', methods=['GET'])
def verifyUser(verify_uuid):
	try:
		User.verify(verify_uuid)
		# If no exceptions happen, redirect them to the login page with success
		flash('You have successfully verified your email. You may now log in.', 'success')
		return  redirect('/login?type=user')
	except UserException:
		# This means we didn't find the verification
		abort(404)
	except Exception:
		# This means an error happened, most probably something SQL
		abort(500)

@app.route('/verify_org/<verify_uuid>', methods=['GET'])
def verifyOrg(verify_uuid):
	try:
		Organization.verify(verify_uuid)

		# If no exceptions happen, redirect them to the login page with success
		flash('You have successfully verified your email. Now please wait for an administrator to accept your access request.', 'success')
		return  redirect('/login?type=org')
	except UserException:
		# This means we didn't find the verification
		abort(404)
	except Exception:
		# This means an error happened, most probably something SQL
		abort(500)

# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# TODO: ADD MORE ERROR HANDLERS