import sqlite3

dbcon = None

def connect():
	if dbcon:
		return
	else:
		dbcon = sqlite3.connect('app.db')
		print('Connected to database.')

def clear_db():
	# Read the clear_db.sql file
	f = open('clear_db.sql', 'r')
	dbcon.executescript(f.read().decode('utf-8'))
	f.close()
	print('Cleared database.')

def init_db():
	# Read the schema.sql file
	f = open('schema.sql', 'r')
	dbcon.executescript(f.read().decode('utf-8'))
	f.close()
	print('Initialized database.')
