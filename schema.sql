CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	dob INTEGER NOT NULL,
	city TEXT NOT NULL,
	emirate TEXT NOT NULL,
	po_box TEXT NOT NULL,
	address_1 TEXT NOT NULL,
	address_2 TEXT NOT NULL,
	phone TEXT NOT NULL,
	email TEXT NOT NULL,
	password TEXT NOT NULL,
	isAdmin INTEGER NOT NULL
);