# Library imports
from flask import Flask, render_template, request
app = Flask(__name__, static_url_path='/assets', static_folder='assets')


# Flask routes
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html', type=request.args.get('type'))

@app.route('/register')
def register():
    return render_template('register.html', type=request.args.get('type'))