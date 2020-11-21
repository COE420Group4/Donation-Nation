import sqlite3

class DB:
	def connect(self):
		return sqlite3.connect('app.db')

	def clear_db(self):
		# Read the clear_db.sql file
		dbcon = self.connect()
		f = open('clear_db.sql', 'r')
		dbcon.executescript(f.read())
		dbcon.close()
		f.close()
		print('Cleared database.')

	def init_db(self):
		# Read the schema.sql file
		dbcon = self.connect()
		f = open('schema.sql', 'r')
		dbcon.executescript(f.read())
		dbcon.close()
		f.close()
		print('Initialized database.')

	def execute_p(self, query, paramters):
		self.dbcon.execute(query, paramters)
