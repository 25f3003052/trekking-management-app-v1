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
