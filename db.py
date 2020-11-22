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


	# def populate_org(self):
	# 	#Populate the organizations table with values
	# 	dbcon = self.connect()
	# 	RC_info = (1, 'd7163a6d-ebf9-4b12-90c8-ba91db375c7c', 'Red Crescent', 1,
	# 	0, 111111111, 'Abu Dhabi', 'Abu Dhabi', '11111', 'Abu Dhabi', 'Al Nahyan', '800733','RC_Logo',
	# 	'redcrescent@gmail.com', 'redcrescentpwd')
	# 	EC_info = (2, '4c43606c-6a42-482d-a195-615b4efcc9a3', 'Emirates Charity',
	# 	2, 0, 222222222, 'Abu Dhabi', 'Abu Dhabi', '22222', 'Abu Dhabi', 'Mushrif', '800600','EC_Logo',
	# 	'emiratescharity@gmail.com', 'emiratescharitypwd')
	# 	KBZ_info = (3, '70815c4e-c816-4fb8-913e-72f20056d1e4', 'Khalifa Bin Zayed'
	# 	Al Nahyan Foundation', 3, 0, 333333333, 'Abu Dhabi', 'Abu Dhabi', '22222', 'Abu Dhabi', 'Al
	# 	Bateen', '028855588','KBZ_Logo', 'kbz@gmail.com', 'kbzpwd')
	# 	dbcon.execute("INSERT INTO organizations (id, UUID, org_name, req_id,
	# 	status, license_no, city, emirate, po_box, address_1, address_2, phone, logo, email, password)
	# 	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", RC_info)
	# 	dbcon.execute("INSERT INTO organizations (id, UUID, org_name, req_id,
	# 	status, license_no, city, emirate, po_box, address_1, address_2, phone, logo, email, password)
	# 	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", EC_info)
	# 	dbcon.execute("INSERT INTO organizations (id, UUID, org_name, req_id,
	# 	status, license_no, city, emirate, po_box, address_1, address_2, phone, logo, email, password)
	# 	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", KBZ_info)
	# 	dbcon.commit()
	# 	dbcon.close()
	# 	print('Populated organizations database.')
