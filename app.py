# DataHandler
from werkzeug.utils import redirect
from DataHandler import User, UserException

# Library imports
import os
from flask import Flask, session, render_template, request, abort, redirect
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
					return 'Success'
				except UserException as ue:
					# TODO: Add flask flashing
					print(ue)
					abort(400) # ! CHANGE ME
			elif request.form.get('type') == 'org':
				abort(404)
			else:
				abort(400)
		else:
			return render_template('login.html', type=request.args.get('type'))
	else:
		return 'Success'

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if request.form.get('type') == 'user':
			try:
				User.insert(request.form)
				return 'Success'
			except UserException as ue:
				# TODO: Add flask flashing
				print(ue)
				abort(400) # ! CHANGE ME
		elif request.form.get('type') == 'org':
			pass
		else:
			abort(400)
	else:
		return render_template('register.html', type=request.args.get('type'))

@app.route('/orgs', methods=['GET'])
def orgs():
	return render_template('orgs.html')

@app.route('/items', methods=['GET', 'POST'])
def items():
	return render_template('items.html', type=request.args.get('type'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	return render_template('admin.html')

@app.route('/addItem', methods=['GET', 'POST'])
def donate():
	return render_template('addItem.html', method=['GET', 'POST'])

@app.route('/orgProfile', methods=['GET'])
def orgProfile():
	return render_template('orgProfile.html')

@app.route('/userProfile', methods=['GET'])
def userProfile():
	if 'isLoggedIn' in session:
		return render_template('userProfile.html', userData=session['isLoggedIn'])
	else:
		# TODO: flask flashing
		return redirect('/login')

# The user information page from organization's perspective
# * This is an example of how we pass variables in the URL path
@app.route('/user/<uuid>', methods=['GET'])
def viewUser(uuid):
	# TODO: only organizations can see this page
	# Fetch user info
	user_info = User.fetchByUUID(uuid)
	if user_info is not False:
		return render_template('viewUser.html', userData=user_info)
	else:
		abort(404)

#The organization information page from user's perspective
@app.route('/viewOrg', methods=['GET'])
def viewOrg():
	return render_template('viewOrg.html')

# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

