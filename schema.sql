CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	UUID TEXT NOT NULL,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	dob TEXT NOT NULL,
	city TEXT NOT NULL,
	emirate TEXT NOT NULL,
	po_box TEXT NOT NULL,
	address_1 TEXT NOT NULL,
	address_2 TEXT NOT NULL,
	phone TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	isAdmin INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS organizations (
admin_id TEXT NOT NULL,
org_name TEXT PRIMARY KEY, /*made this a primary key bc we use it to */
req_id INTEGER NOT NULL,
status INTEGER NOT NULL,
license_no INTEGER NOT NULL,
city TEXT NOT NULL,
emirate TEXT NOT NULL,
po_box TEXT NOT NULL,
address_1 TEXT NOT NULL,
address_2 TEXT NOT NULL,
phone TEXT NOT NULL UNIQUE,
email TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
FOREIGN KEY (admin_id)
REFERENCES users (id)
);
CREATE TABLE IF NOT EXISTS items (
item_name TEXT NOT NULL,
id INTEGER PRIMARY KEY,
category TEXT NOT NULL,
condition TEXT NOT NULL,
description TEXT NOT NULL,
category TEXT NOT NULL,
org_name TEXT NOT NULL,
time_submitted TEXT NOT NULL,
pickup_time TEXT NOT NULL,
image BLOB NOT NULL
FOREIGN KEY (org_name)
REFERENCES org_req_access (org_name)
);