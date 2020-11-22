CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	UUID TEXT NOT NULL UNIQUE,
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
	isAdmin INTEGER NOT NULL,
	isVerified INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS organizations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	UUID TEXT NOT NULL UNIQUE,
	org_name TEXT NOT NULL,
	req_id INTEGER NOT NULL,
	status INTEGER NOT NULL,
	license_no INTEGER NOT NULL,
	city TEXT NOT NULL,
	emirate TEXT NOT NULL,
	po_box TEXT NOT NULL,
	address_1 TEXT NOT NULL,
	address_2 TEXT NOT NULL,
	phone TEXT NOT NULL UNIQUE,
	logo BLOB NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL
);

-- For email verification. It is in its own table so we can delete the rows after the user verifies their email.
CREATE TABLE IF NOT EXISTS verifications (
	user_id INTEGER PRIMARY KEY,
	verification_uuid TEXT UNIQUE NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS items (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	item_name TEXT NOT NULL,
	category TEXT NOT NULL,
	condition TEXT NOT NULL,
	description TEXT NOT NULL,
	org_id TEXT NOT NULL,
	user_id TEXT NOT NULL,
	time_submitted TEXT NOT NULL,
	pickup_time TEXT NOT NULL,
	image BLOB NOT NULL,
	FOREIGN KEY (org_id) REFERENCES organizations (UUID),
	FOREIGN KEY (user_id) REFERENCES users (UUID)
);