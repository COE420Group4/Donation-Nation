import sqlite3
import uuid
import hashlib
from base64 import standard_b64encode as b64
from datetime import datetime
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

	def populate(self):
		# Let's create some users
		dbcon = self.connect()
		cur = dbcon.cursor()
		passwd = hashlib.sha256(b'a').hexdigest()
		john_uuid = str(uuid.uuid4())
		donald_uuid = str(uuid.uuid4())
		rich_uuid = str(uuid.uuid4())
		margeret_uuid = str(uuid.uuid4())
		jake_uuid = str(uuid.uuid4())
		cur.execute('INSERT INTO users (UUID,first_name,last_name,dob,city,emirate,po_box,address_1,address_2,phone,email,password,isAdmin,isVerified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (john_uuid, "John", "Doe", "24/11/1999", "Sharjah", "Sharjah", "75362", "Al Mamzar Building 1, Al Taawun", "Besides Burger King", "0502345671", "admin@email.com", passwd, 1, 1)) # admin user
		cur.execute('INSERT INTO users (UUID,first_name,last_name,dob,city,emirate,po_box,address_1,address_2,phone,email,password,isAdmin,isVerified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (donald_uuid, "Donald", "Duck", "3/1/1947", "Muweileh", "Dubai", "66634", "House 374B. Muweileh Street", "Besides McDonalds", "0508764563", "donald@email.com", passwd, 0, 1))
		cur.execute('INSERT INTO users (UUID,first_name,last_name,dob,city,emirate,po_box,address_1,address_2,phone,email,password,isAdmin,isVerified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (rich_uuid, "Richy", "McRich", "24/11/1999", "Jumeira", "Dubai", "133700", "Burj Khalifa, Apartment 9405", "In Burj Khalifa, yo", "0501111111", "rich@email.com", passwd, 0, 1))
		cur.execute('INSERT INTO users (UUID,first_name,last_name,dob,city,emirate,po_box,address_1,address_2,phone,email,password,isAdmin,isVerified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (margeret_uuid, "Margeret", "Thatcher", "1/1/1200", "Al Ain", "Abu Dhabi", "12345", "Some building with some number", "Next to a road somewhere", "0506666666", "margeret@email.com", passwd, 0, 1))
		cur.execute('INSERT INTO users (UUID,first_name,last_name,dob,city,emirate,po_box,address_1,address_2,phone,email,password,isAdmin,isVerified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (jake_uuid, "Jake", "Peralta", "20/6/1981", "Al Ain", "Abu Dhabi", "33344", "An awesome police station.", "A really noice police station.", "0509737542", "jake@email.com", passwd, 0, 1))
		dbcon.commit()

		# Let's create some organizations
		red_cresent_uuid = str(uuid.uuid4())
		dubai_cares_uuid = str(uuid.uuid4())
		uae_aid_uuid = str(uuid.uuid4())
		red_crescent_pic = b64(open('./assets/red.jpeg', 'rb').read())
		dubai_cares_pic = b64(open('./assets/cares.jpg', 'rb').read())
		uae_aid_pic = b64(open('./assets/aid.jpg', 'rb').read())
		cur.execute('INSERT INTO organizations (UUID,name,status,license_no,city,emirate,po_box,address_1,address_2,phone,logo,email,password) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (red_cresent_uuid, 'Red Crescent', 2, '222-333-444', 'Jumeira', 'Dubai', '112233', 'Somewhere', 'Someplace', '062224444', red_crescent_pic, 'contact@redcrescent.org', passwd))
		cur.execute('INSERT INTO organizations (UUID,name,status,license_no,city,emirate,po_box,address_1,address_2,phone,logo,email,password) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (dubai_cares_uuid, 'Dubai Cares', 2, '555-777-666', 'Sharjah', 'Sharjah', '56473', 'Somewhere', 'Someplace', '065559999', dubai_cares_pic, 'contact@dubaicares.org', passwd))
		cur.execute('INSERT INTO organizations (UUID,name,status,license_no,city,emirate,po_box,address_1,address_2,phone,logo,email,password) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (uae_aid_uuid, 'UAE Aid', 2, '111-999-888', 'Al Ain', 'Abu Dhabi', '74573', 'Somewhere', 'Someplace', '063331111', uae_aid_pic, 'contact@uaeaid.org', passwd))
		cur.execute('INSERT INTO organizations (UUID,name,status,license_no,city,emirate,po_box,address_1,address_2,phone,logo,email,password) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (str(uuid.uuid4()), 'Testing Org 1', 1, '333-333-333', 'Al Ain', 'Abu Dhabi', '23451', 'Somewhere', 'Someplace', '061231231', b'', 'contact@somewhere.org', passwd))
		cur.execute('INSERT INTO organizations (UUID,name,status,license_no,city,emirate,po_box,address_1,address_2,phone,logo,email,password) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (str(uuid.uuid4()), 'Testing Org 2', 0, '333-333-333', 'Al Ain', 'Abu Dhabi', '523456', 'Somewhere', 'Someplace', '064564563', b'', 'contact@nowhere.org', passwd))
		dbcon.commit()

		# Let's create some items
		shirt_uuid = str(uuid.uuid4())
		books_uuid = str(uuid.uuid4())
		tools_uuid = str(uuid.uuid4())
		lego_set_uuid = str(uuid.uuid4())
		bedsheets_uuid = str(uuid.uuid4())
		children_socks_uuid = str(uuid.uuid4())
		barbie_set_uuid = str(uuid.uuid4())
		software_engineering_textbook_uuid = str(uuid.uuid4())
		die_hard_movie_uuid = str(uuid.uuid4())
		shirt_pic = b64(open('./assets/shirt.jpg', 'rb').read())
		books_pic = b64(open('./assets/book.jpg', 'rb').read())
		tools_pic = b64(open('./assets/tools.jpg', 'rb').read())
		lego_set_pic = b64(open('./assets/lego.jpg', 'rb').read())
		bedsheets_pic = b64(open('./assets/sheets.jpg', 'rb').read())
		children_socks_pic = b64(open('./assets/socks.jpg', 'rb').read())
		barbie_set_pic = b64(open('./assets/barbie.jpg', 'rb').read())
		software_engineering_textbook_pic = b64(open('./assets/textbook.jpg', 'rb').read())
		die_hard_pic = b64(open('./assets/diehard.jpg', 'rb').read())
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,0)', (shirt_uuid,'Red Hoodie','Clothes','New','A red hoodie.',red_cresent_uuid,donald_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',shirt_pic))
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,1)', (books_uuid,'Children\'s Books','Books','Lightly used','A children\'s book about the tooth fairy.',red_cresent_uuid,donald_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',books_pic))
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,-1)', (tools_uuid,'Construction Tools','Toys','New','A set of construction tools.',red_cresent_uuid,margeret_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',tools_pic))
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,2)', (lego_set_uuid,'Millennium Falcon Lego Set','Toys','New','A premium millennium falcon lego set.',red_cresent_uuid,donald_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',lego_set_pic))
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,-1)', (bedsheets_uuid,'Bedsheets','Linens','Heavily used','Some worn bedsheets.',dubai_cares_uuid,donald_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',bedsheets_pic))
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,0)', (children_socks_uuid,'Children Socks','Clothes','New','Some colorful children socks.',dubai_cares_uuid,margeret_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',children_socks_pic))
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,0)', (barbie_set_uuid,'Barbie Set','Toys','Lightly used','Some barbie toys. Mostly without heads.',uae_aid_uuid,margeret_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',barbie_set_pic))
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,3)', (software_engineering_textbook_uuid,'Software Engineering Book','Books','Lightly used','A very useful and well needed book in modern society.',red_cresent_uuid,donald_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',software_engineering_textbook_pic))
		cur.execute('INSERT INTO items (UUID,item_name,category,condition,description,org_id,user_id,time_submitted,pickup_time,image,status) VALUES (?,?,?,?,?,?,?,?,?,?,-1)', (die_hard_movie_uuid,'Die Hard Movie','Books','Lightly used','An awesome christmas movie. The best ever.',red_cresent_uuid,jake_uuid,datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),'Morning (8:00 AM - 11:00 AM)',die_hard_pic))
		dbcon.commit()