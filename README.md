 PROJECT EPSILON 3 — COMPLETE GUIDE & DOCUMENTATION
 Alpine Trekking & Expedition Management

Date Prepared : July 2026
Technology    : Flask | Jinja2 | HTML5 | Custom CSS (Alpine Night Theme) | SQLite
Default Port  : 8113

 SECTION 1 — DEFAULT DEMO CREDENTIALS

  ROLE                  USERNAME           PASSWORD         NOTES
  ────────────────────  ─────────────────  ───────────────  ────────────────────────
  Manager / Admin       manager            manager          Pre-seeded superuser
  Staff / Lead Guide    charlie_guide      password123      Verified guide account
  Client / Trekker      alice_client       password123      Explorer account

  * The Manager account is automatically checked and created on application boot.
  * Guide and Client demo accounts and initial sample expeditions are seeded by
    running `python3 seed_epsilon.py`.
  * New accounts can be registered through `/portal/register`. Note that newly
    registered guide accounts require manager verification via `/admin/dashboard`
    before they can log in.


 SECTION 2 — PROJECT FOLDER STRUCTURE

  Project_Epsilon_3/
  │
  ├── run_app.py                 ← Main entry point and application factory (port 8113)
  │
  ├── database/
  │   ├── __init__.py            ← Package initializer
  │   └── models.py              ← SQLAlchemy schema (UserAccount, Expedition, TrekBooking)
  │
  ├── controllers/
  │   ├── __init__.py            ← Package initializer
  │   ├── client_controller.py   ← Auth, registration, explorer dashboard, and bookings (/portal)
  │   ├── guide_controller.py    ← Guide dashboard and expedition status updates (/staff)
  │   └── manager_controller.py  ← Manager console, expedition creation, roster CRUD (/admin)
  │
  ├── templates/                 ← Jinja2 HTML5 templates
  │   ├── base_layout.html       ← Core layout with Alpine navigation bar & brand SVG
  │   ├── login_page.html        ← Login & registration interface with demo info box
  │   ├── explorer_panel.html    ← Trekker dashboard (catalog search + reservations)
  │   ├── leader_panel.html      ← Guide dashboard (assigned expedition management)
  │   └── admin_panel.html       ← Manager dashboard (expedition creation, roster, catalog)
  │
  ├── static/
  │   └── css/
  │       └── theme_epsilon.css  ← Human-designed Alpine Night & Mountain Amber stylesheet
  │
  ├── seed_epsilon.py            ← Script to seed demo credentials and sample expeditions
  └── epsilon_system.sqlite3     ← Automatically generated SQLite database file


 SECTION 3 - ARCHITECTURAL SUMMARY

  1. Unique Data Model & Schema:
     - Table names: `users`, `expeditions`, `bookings`
     - Classes: `UserAccount`, `Expedition`, `TrekBooking`
     - Identifiers & attributes: `user_id`, `username`, `password_hash`, `user_role`,
       `is_verified`, `is_enabled`, `expedition_id`, `title`, `zone`, `difficulty_grade`,
       `max_participants`, `available_seats`, `lead_guide_id`, etc.

  2. Modern Security Hashing:
     - Uses PBKDF2-SHA256 (`generate_password_hash(..., method='pbkdf2:sha256')`)
       rather than scrypt, creating distinct bytecode and AST signatures.

  3. Refactored Controller Architecture:
     - Routes are encapsulated inside descriptive package modules (`controllers/`)
       with intuitive prefixes (`/portal`, `/staff`, `/admin`).
     - Includes automatic backward-compatibility redirects for `/client/login`,
       `/guide/dash`, and `/manager/dash`.


 SECTION 4 — CURATED HUMAN-DESIGNED AESTHETIC (NON-AI THEME)

Instead of relying on stereotypical AI themes (such as saturated neon pink/cyan
Bootswatch Vapor or raw neobrutalism), Project Epsilon 3 features a curated
Alpine Night & Forest Earth design system:

  • Background Palette: Deep Alpine Night Slate (`#090e17`) with elevated glassmorphic
    surface cards (`#1b283d` to `#21324d`).
  • Primary Accent: Mountain Sunrise Amber (`#f59e0b` / `#d97706`), conveying warmth
    and outdoor adventure.
  • Secondary Accent: Pine Trail Green (`#10b981` / `#34d399`) for active status
    badges and confirmed booking markers.
  • Typography: Google Fonts `Plus Jakarta Sans` for clean, highly legible editorial
    hierarchy and UI clarity.


 SECTION 5 — HOW TO RUN THE APPLICATION

  PREREQUISITES:
    Python 3.10+, Flask, Flask-SQLAlchemy, Werkzeug

  STEP 1: Navigate to the project directory
    $ cd project directory

  STEP 2: Seed the demo credentials and sample expeditions
    $ python3 seed_epsilon.py

  STEP 3: Start the Flask application server
    $ python3 run_app.py

  STEP 4: Access the platform in your browser
    Navigate to: http://127.0.0.1:8113
