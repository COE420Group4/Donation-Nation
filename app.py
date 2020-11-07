# Library imports
from flask import Flask, render_template, request
app = Flask(__name__, static_url_path='/assets', static_folder='assets')


# Flask routes
@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', type=request.args.get('type'))

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    return render_template('addItem.html')

# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
