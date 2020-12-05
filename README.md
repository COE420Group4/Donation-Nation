# COE420Project

## Running The Project

You need **Python 3** to get started.
To install the libraries used in the project, run the following command:

```bash
pip install flask sqlite3 hashlib
```

## Functional Requirements

- [x] **R1: Login to system**
  - [x] Frontend
  - [x] Database setup
  - [x] Verifying credentials + session setup
- [x] **R2: User Sign up**
  - [x] Frontend
  - [x] Database setup
  - [x] Verifying information
  - [x] Insertion into database
  - [x] Sending verification email
- [x] **R3: Organization Request access**
  - [x] Frontend
  - [x] Database setup
  - [x] Verifying information
  - [x] Insertion into database
  - [x] Sending verification email
  - [x] Being verified by admin
- [x] **R4: Verify Email**
  - [x] Frontend
  - [x] Database setup
  - [x] Backend logic to verify account
- [x] **R5: Offer item**
  - [x] Frontend
  - [x] Database setup
  - [x] Verifying information
  - [x] Inserting item into db
  - [x] Sending notification email
- [x] **R6: View donor info**
  - [x] Frontend
  - [x] Database setup
  - [x] Fetching info from database
- [x] **R7: Remove Item**
  - [x] Frontend
  - [x] Verifying information
  - [x] Logical checks
  - [x] Removing item from db
- [x] **R8: List Donated items**
  - [x] Frontend
  - [x] Database setup
  - [x] Fetching info from database
- [ ] **R9: List Offered Items**
  - [ ] Frontend
  - [x] Database setup
  - [ ] Fetching info from database
- [ ] **R10: Approve Donated Item**
  - [ ] Frontend
  - [ ] Verifying information
  - [ ] Mark item as approved
  - [ ] Send emails
- [ ] **R11: Reject Donated Item**
  - [ ] Frontend
  - [ ] Verifying information
  - [ ] Mark item as rejected
  - [ ] Send email with new suggested time
- [ ] **R12: Approve Pickup Time**
  - [x] Frontend
  - [x] Verifying information
  - [ ] Mark item as approved
  - [ ] Send emails
- [ ] **R13: Reject Pickup Time**
  - [x] Frontend
  - [x] Verifying information
  - [ ] Mark new pickup time as rejected
  - [ ] Send email with new suggested time
- [x] **R14: List Organizations**
  - [x] Frontend
  - [x] Fetch information from db
- [x] **R15: List Organization Access Requests**
  - [x] Frontend
  - [x] Fetch information from db
- [x] **R16: Approve Organization Access Request**
  - [x] Frontend
  - [x] Verifying information
  - [x] Mark organization as approved
  - [x] Send email
- [x] **R17: Reject Organization Access Request**
  - [x] Frontend
  - [x] Verifying information
  - [x] Mark organization as rejected
  - [x] Send email

### Components

- Bootstrap v4 for the design/framework
- FontAwesome for the icons
- Animate.css for the animations
- Jinja2 for the templates

## TODO

- [x] Setup files
- [x] Build flask skeleton
- [x] Setup flask templates
- [x] Finish planning routes
- [x] Finish database structure
- [x] Finish db.py
- [ ] Finish all the frontend
- [x] Finish login/registration for users
- [x] Finish organization registration
- [x] Finish email sending code
- [ ] Finish the listing functional requirements
