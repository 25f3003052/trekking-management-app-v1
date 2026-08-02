from flask import render_template, redirect, session, request, flash
from app import app
from models import * 
from datetime import datetime, date as date_class


# home page route
@app.route('/')
def home():
    return render_template('index.html')

# ----------------- Register ------------------

@app.route('/register')
def register():
    return render_template('register.html')

# it will handle the data comming from register_form.html
@app.route('/register', methods=['POST'])
def register_post():
    role = request.form.get('role', 'trekker')
    user_name = request.form.get('username')
    name = request.form.get('name')
    email_id = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")

    if role == 'staff':
        experience = request.form.get("experience")
        existing_staff = Staff.query.filter((Staff.user_name == user_name) | (Staff.email_id == email_id)).first()
        existing_user = User.query.filter((User.user_name == user_name) | (User.email_id == email_id)).first()

        if existing_staff or existing_user:
            flash('Account with this username or email already exists...', category='error')
            return redirect('/register')

        new_staff = Staff(
            user_name=user_name,
            name=name,
            email_id=email_id,
            phone=phone,
            experience=experience
        )
        new_staff.set_password(password)
        db.session.add(new_staff)
        db.session.commit()
        flash('Staff registration submitted! Please wait for admin approval.', category='success')
        return redirect('/login')

    address = request.form.get("address")
    pincode = request.form.get("pincode")
    age = request.form.get("age")
    gender = request.form.get("gender")

    existing_user = User.query.filter((User.user_name == user_name) | (User.email_id == email_id)).first()
    existing_staff = Staff.query.filter((Staff.user_name == user_name) | (Staff.email_id == email_id)).first()

    if existing_user or existing_staff:
       flash('Account with this username or email already exists...', category='error')
       return redirect('/register')
    
    new_user = User(user_name = user_name, name=name, gender = gender, phone=phone, address=address, age = age, pincode=pincode, email_id = email_id)

    new_user.set_password(password) # used to hash the password
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successfull! Please log in...', category='success')
    return redirect('/login')

@app.route('/register_staff')
def register_staff():
    return render_template('register_staff.html')

@app.route('/register_staff', methods=['POST'])
def register_staff_post():
    username = request.form.get("username")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    experience = request.form.get("experience")

    existing = Staff.query.filter((Staff.user_name == username) | (Staff.email_id == email)).first()
    if existing:
        flash("Staff with this username or email already exists.", category="error")
        return redirect("/register_staff")

    new_staff = Staff(user_name=username, name=name, email_id=email, phone=phone, experience=experience)
    new_staff.set_password(password)
    db.session.add(new_staff)
    db.session.commit()
    flash("Registration submitted! Please wait for admin approval.", category="success")
    return redirect("/login")



# ------------------- Login -------------------- 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    role = request.form.get('role')
    username = request.form.get('username')
    password = request.form.get('password')

    if not role:
        flash('Please select a role.', category='error')
        return redirect('/login')
    
    if not username or not password:
        flash('Fill both username and password.', category='error')
        return redirect('/login')
    
    if role == 'admin':
        user = User.query.filter_by(user_name = username, is_admin=True).first()
        if not user:
            flash('No admin found with this username', category='error')
            return redirect('/login')
        
        if not user.check_password(password):
            flash('Incorrect admin password', category='error')
            return redirect('/login')
        
        session['user_id'] = user.id
        session['role'] = 'admin'
        flash('Welcme Admin...', category='success')
        return redirect('/admin')
    
    if role == "staff":
        staff = Staff.query.filter_by(user_name=username).first()
        if not staff:
            flash("No staff found with this username.", "error")
            return redirect('/login')
        if staff.is_blocked:
            return redirect('/blocked')
        if not staff.is_approved:
            flash("Your account is pending admin approval.", "error")
            return redirect('/login')
        if not staff.check_password(password):
            flash("Incorrect staff password.", "error")
            return redirect('/login')
        session['staff_id'] = staff.id
        session['role'] = 'staff'
        flash(f"Welcome {staff.name}!", "success")
        return redirect('/staff_dashboard')
    
    if role == "trekker":
        user = User.query.filter_by(user_name=username, is_admin=False).first()
        if not user:
            flash("No trekker found with this username.", "error")
            return redirect('/login')
        if user.is_blocked:
            return redirect('/blocked')
        if not user.check_password(password):
            flash("Incorrect password.", "error")
            return redirect('/login')
        session['user_id'] = user.id
        session['role'] = 'trekker'
        flash(f"Welcome {user.name}!", "success")
        return redirect('/user')
    
    flash('Invalid login credentials', 'error')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out...', category='success')
    return redirect('/')


# --------------- Dashboards ----------------

# admin routes
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session:
        flash('Please log in.', category='error')
        return redirect('/login')
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('Access denied. Admins Only.', category='error')
        return redirect('/login')
    treks = Trek.query.all() # storing all the info related to Trek table
    staff_list = Staff.query.all() 
    approved_staff = Staff.query.filter_by(is_approved=True, is_blocked=False).all()
    trekkers = user.query.filter_by(is_admin=False).all()
    bookings = Booking.query.all()
    return render_template('admin_dashboard.html', user=user, treks=treks, staff_list=staff_list, approved_staff=approved_staff, trekkers=trekkers, bookings=bookings) # will be used in admin_dashboard.html frontend render part 

# --- Assign Staff to Trek (inline from dashboard) ---
@app.route('/assign_staff/<int:trek_id>', methods=['POST'])
def assign_staff(trek_id):
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        flash('Access denied.', category='error')
        return redirect('/login')
    
    trek = Trek.query.get_or_404(trek_id)
    staff_id = request.form.get('staff_id')
    if staff_id:
        staff = Staff.query.get_or_404(int(staff_id))
        if not staff.is_approved or staff.is_blocked:
            flash('Only approved and active staff can be assigned.', category='error')
            return redirect('/admin')
        trek.assigned_staff_id = staff.id
        flash(f"Staff '{staff.name}' assigned to '{trek.trek_name}'!", category='success')
    else:
        trek.assigned_staff_id = None
        flash(f'Staff removed from "{trek.trek_name}".', category='success')
    
    db.session.commit()
    return redirect('/admin')

# --- Add Trek ---
@app.route('/add_trek', methods=['GET', 'POST'])
def add_trek():
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect('/login')
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        flash('Access denied.', 'error')
        return redirect('/login')

    staff_list = Staff.query.filter_by(is_approved=True, is_blocked=False).all()

    if request.method == 'GET':
        return render_template('add_trek.html', user=user, staff_list=staff_list)

    trek_name = request.form.get('trek_name')
    location = request.form.get('location')
    difficulty = request.form.get('difficulty')
    duration_days = request.form.get('duration_days')
    total_slots = request.form.get('total_slots')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    description = request.form.get('description')
    assigned_staff_id = request.form.get('assigned_staff_id')
    status = request.form.get('status', 'Pending')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else date_class.today()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else date_class.today()
    except:
        flash("Invalid date format.", "error")
        return redirect('/add_trek')

    slots = int(total_slots) if total_slots else 20

    new_trek = Trek(
        trek_name=trek_name, location=location, difficulty=difficulty,
        duration_days=int(duration_days) if duration_days else 1,
        total_slots=slots, available_slots=slots,
        status=status, start_date=start_date, end_date=end_date,
        description=description,
        assigned_staff_id=int(assigned_staff_id) if assigned_staff_id else None,
        created_by=session['user_id']
    )
    db.session.add(new_trek)
    db.session.commit()
    flash("Trek added successfully!", "success")
    return redirect("/admin")

