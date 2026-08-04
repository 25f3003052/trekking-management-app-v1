# TrekTrail - Trekking Management System

**Prepared by:** Shivansh Sharma

TrekTrail is a Flask-based trekking management and booking web application. It provides a centralized platform where administrators can manage treks, staff, trekkers, and bookings; staff can manage assigned treks and participants; and trekkers can search, book, cancel, and track trekking activities.

## Problem Statement

Trekking activities require proper coordination between administrators, trekking staff, and participants. Without a centralized system, it becomes difficult to manage trek schedules, available slots, staff assignment, booking status, participant records, and trek progress.

This project solves that problem by providing a role-based web application for managing the complete trekking workflow.

## Proposed Solution

TrekTrail divides the application into three main roles:

- **Admin:** Manages treks, staff approvals, staff assignment, trekkers, and all bookings.
- **Staff:** Views assigned treks, checks participants, and updates trek status.
- **Trekker/User:** Registers, logs in, searches treks, books open treks, cancels eligible bookings, edits profile, and views booking history.

The application uses Flask for the backend, SQLAlchemy ORM for database interaction, SQLite for storage, and Jinja2 templates with custom CSS for the frontend.

## Features

- Role-based login for admin, staff, and trekkers
- Trekker and staff registration
- Staff approval and rejection by admin
- Secure password hashing using Werkzeug
- Admin dashboard for managing treks, staff, trekkers, and bookings
- Add, edit, delete, and assign staff to treks
- Staff dashboard for assigned treks and participant tracking
- Trek status updates by assigned staff
- Trek booking and cancellation workflow
- Trekker booking history
- Admin search for treks, staff, and trekkers
- Trekker search and filter for available treks
- Block/unblock functionality for staff and trekkers
- SQLite database integration

## Technology Stack

| Layer | Technology |
| --- | --- |
| Backend | Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Password Security | Werkzeug |
| Frontend | HTML, Jinja2 templates, CSS |
| Validation | HTML validation and `static/form-validation.js` |

## Project Structure

```text
Tracking/
+-- app.py
+-- config.py
+-- models.py
+-- routes.py
+-- requirements.txt
+-- report.pdf
+-- README.md
+-- instance/
|   +-- Treck.db
+-- static/
|   +-- style.css
|   +-- nav.css
|   +-- form-validation.js
|   +-- pages/
+-- templates/
    +-- layout.html
    +-- nav.html
    +-- index.html
    +-- login.html
    +-- register.html
    +-- admin_dashboard.html
    +-- staff_dashboard.html
    +-- user_dashboard.html
```

## Database Models

### User

Stores admin and trekker accounts.

Important fields:

- `id`
- `user_name`
- `name`
- `email_id`
- `password`
- `phone`
- `age`
- `gender`
- `pincode`
- `address`
- `is_admin`
- `is_blocked`

Relationship:

- One user can have many bookings.

### Staff

Stores staff/guide account details.

Important fields:

- `id`
- `user_name`
- `name`
- `email_id`
- `password`
- `phone`
- `experience`
- `is_approved`
- `is_blocked`

Relationship:

- One staff member can be assigned to many treks.

### Trek

Stores trek information created by admin.

Important fields:

- `id`
- `trek_name`
- `location`
- `difficulty`
- `duration_days`
- `available_slots`
- `total_slots`
- `status`
- `start_date`
- `end_date`
- `description`
- `assigned_staff_id`
- `created_by`

Relationship:

- A trek may have one assigned staff member.
- A trek can have many bookings.

### Booking

Stores trekker booking records.

Important fields:

- `id`
- `user_id`
- `trek_id`
- `booking_date`
- `status`

Relationship:

- A booking belongs to one user and one trek.

## ER Diagram

```text
User (1) --------< Booking >-------- (1) Trek
  |                                      |
  | created_by                           | assigned_staff_id
  |                                      |
  +-------------------------------> Staff

User:
  id PK
  user_name
  email_id
  is_admin
  is_blocked

Staff:
  id PK
  user_name
  email_id
  is_approved
  is_blocked

Trek:
  id PK
  trek_name
  assigned_staff_id FK
  created_by FK

Booking:
  id PK
  user_id FK
  trek_id FK
```

## Application Flow

1. Visitor opens the home page.
2. User registers as a trekker or staff member.
3. Staff registration waits for admin approval.
4. User logs in by selecting a role: admin, staff, or trekker.
5. Admin manages treks, staff approvals, trekker accounts, and bookings.
6. Admin assigns approved staff to treks.
7. Staff views assigned treks and manages trek progress.
8. Trekker views available treks and books open treks.
9. Trekker can cancel a booking before the trek is closed or completed.
10. Staff marks treks as started or completed.
11. Completed treks update related booking statuses.

## Main Routes

| Route | Method | Description |
| --- | --- | --- |
| `/` | GET | Home page |
| `/register` | GET/POST | Register trekker or staff |
| `/register_staff` | GET/POST | Staff registration |
| `/login` | GET/POST | Role-based login |
| `/logout` | GET | Logout and clear session |
| `/admin` | GET | Admin dashboard |
| `/add_trek` | GET/POST | Add new trek |
| `/edit_trek/<trek_id>` | GET/POST | Edit trek details |
| `/delete_trek/<trek_id>` | POST | Delete trek |
| `/assign_staff/<trek_id>` | POST | Assign staff to trek |
| `/approve_staff/<staff_id>` | POST | Approve staff account |
| `/reject_staff/<staff_id>` | POST | Reject staff account |
| `/staff/block/<staff_id>` | POST | Block staff |
| `/staff/unblock/<staff_id>` | POST | Unblock staff |
| `/staff/edit/<staff_id>` | GET/POST | Edit staff details |
| `/staff/details/<staff_id>` | GET | View staff details |
| `/trekker/block/<trekker_id>` | POST | Block trekker |
| `/trekker/unblock/<trekker_id>` | POST | Unblock trekker |
| `/trekker/delete/<trekker_id>` | POST | Delete trekker |
| `/trekker/history/<trekker_id>` | GET | View trekker booking history |
| `/admin/search` | GET | Admin search |
| `/all_bookings` | GET | View all bookings |
| `/staff_dashboard` | GET | Staff dashboard |
| `/trek_participants/<trek_id>` | GET | View trek participants |
| `/update_trek_status/<trek_id>` | GET/POST | Update trek status |
| `/mark_trek_started/<trek_id>` | POST | Mark trek as started |
| `/mark_trek_completed/<trek_id>` | POST | Mark trek as completed |
| `/user` | GET | Trekker dashboard |
| `/book_trek/<trek_id>` | POST | Book trek |
| `/cancel_booking/<booking_id>` | POST | Cancel booking |
| `/booking_history` | GET | Trekker booking history |
| `/edit_profile` | GET/POST | Edit trekker profile |
| `/trekker/search` | GET | Search/filter treks |
| `/blocked` | GET | Blocked account warning page |

## Step-by-Step Process to Run the Project

### 1. Open the Project Folder

Open a terminal or PowerShell inside the project directory:

```powershell
cd D:\personal_projects\Current_code_with_teaching\Tracking
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
.\.venv\Scripts\activate.bat
```

### 4. Install Required Packages

```powershell
pip install -r requirements.txt
```

### 5. Run the Flask Application

```powershell
python app.py
```

The application will start on:

```text
http://127.0.0.1:8000
```

### 6. Open the Application in Browser

Visit:

```text
http://127.0.0.1:8000
```

### 7. Login as Default Admin

When the app runs, it automatically creates a default admin account if it does not already exist.

```text
Role: Admin
Username: admin
Password: admin
```

## Recommended Testing Flow

1. Start the application using `python app.py`.
2. Login as admin using the default credentials.
3. Register a staff account from the registration page.
4. Approve the staff account from the admin dashboard.
5. Add a trek and assign approved staff to it.
6. Register a trekker account.
7. Login as trekker and book an open trek.
8. Login as staff and view assigned trek participants.
9. Update trek status as started or completed.
10. Check booking history from trekker and admin views.

## Business Rules

- Staff cannot log in until approved by admin.
- Blocked staff and trekkers cannot access their dashboards.
- Only admin can manage treks, staff approvals, users, and all bookings.
- Only assigned staff can update a trek or view its participants.
- Trekkers can book only treks with status `Open`.
- Trekkers cannot book a trek if no slots are available.
- Duplicate active bookings for the same trek are not allowed.
- Trekkers cannot cancel a booking after the trek is `Closed` or `Completed`.
- When a trek is completed, active bookings for that trek are marked as `Completed`.

## Summary

TrekTrail is a complete trekking management system built with Flask and SQLAlchemy. It demonstrates role-based authentication, CRUD operations, booking management, staff approval, user blocking, status tracking, and database relationships. The project provides a practical solution for organizing trekking events and managing the interaction between administrators, staff, and trekkers.
