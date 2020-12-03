# COE420Project

## Running The Project

You need **Python 3** to get started.
To install the libraries used in the project, run the following command:

```bash
pip install flask sqlite3 hashlib
```

## Routes

Routes marked with (!) are visited by the user

**NOTE:** We use UUIDs because a non-functional requirement is security.

- (!) `/login`
- (!) `/register`
- (!) `/verify/<uuid>`
- (!) `/donor/<uuid>`
- (!) `/items`
- (!) `/items/offer`
- `/items/remove`
- `/items/approve`
- `/items/reject`
- `/items/approve_time`
- `/items/reject_time`
- (!) `/orgs`
- (!) `/orgs/<uuid>`
- (!) `/access_requests`
- `/access_requests/approve`
- `/access_requests/reject`

## Database Structure

- USERS
- ITEMS
- ORGS (if user.type == 2)
- ACCESS_REQS

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
- [ ] **R5: Offer item**
  - [x] Frontend
  - [x] Database setup
  - [ ] Verifying information
  - [ ] Inserting item into db
  - [ ] Sending notification email
- [x] **R6: View donor info**
  - [x] Frontend
  - [x] Database setup
  - [x] Fetching info from database
- [ ] **R7: Remove Item**
  - [ ] Frontend
  - [ ] Verifying information
  - [ ] Logical checks
  - [ ] Removing item from db
- [ ] **R8: List Donated items**
  - [x] Frontend
  - [ ] Database setup
  - [ ] Fetching info from database
- [ ] **R9: List Offered Items**
  - [x] Frontend
  - [ ] Database setup
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
  - [ ] Frontend
  - [ ] Verifying information
  - [ ] Mark item as approved
  - [ ] Send emails
- [ ] **R13: Reject Pickup Time**
  - [ ] Frontend
  - [ ] Verifying information
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
- [x] Finish login/signup for users
- [x] Finish organization signup
- [x] Finish email sending code
- [ ] Finish the listing functional requirements
