# Library imports
from flask import Flask, render_template
app = Flask(__name__)


# Flask routes
@app.route('/')
def main():
    return render_template('main.html')