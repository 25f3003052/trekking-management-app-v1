from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from database.models import db, UserAccount, Expedition, TrekBooking

client_controller = Blueprint('client_controller', __name__, url_prefix='/portal')


def _is_client_logged_in() -> bool:
    """Helper check to verify if the current session belongs to a trekker/client."""
    return session.get('user_role') in ('trekker', 'client')


@client_controller.route('/login', methods=['GET', 'POST'])
def handle_login():
    """
    Handles user authentication for all roles (Trekker, Guide, Manager).
    Routes to appropriate dashboards based on role verification.
    """
    if request.method == 'POST':
        username_input = request.form.get('username', '').strip()
        password_input = request.form.get('password', '').strip()

        account = UserAccount.query.filter_by(username=username_input).first()
        if account and account.check_password(password_input):
            if not account.is_enabled:
                return render_template('login_page.html', error_message='Account has been suspended by administration.')
            
            if account.user_role == 'guide' and not account.is_verified:
                return render_template('login_page.html', error_message='Guide account is pending verification by a Manager.')

            session['user_id'] = account.user_id
            session['username'] = account.username
            session['user_role'] = account.user_role

            if account.user_role == 'manager':
                return redirect('/admin/dashboard')
            elif account.user_role == 'guide':
                return redirect('/staff/dashboard')
            else:
                return redirect('/portal/dashboard')

        return render_template('login_page.html', error_message='Invalid username or password credentials.')

    return render_template('login_page.html')


@client_controller.route('/register', methods=['GET', 'POST'])
def handle_registration():
    """
    Allows new trekkers or prospective guides to register for an account.
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        selected_role = request.form.get('role', 'trekker')

        if not username or not password:
            return render_template('login_page.html', show_register=True, reg_error='Username and password are required.')

        if UserAccount.query.filter_by(username=username).first():
            return render_template('login_page.html', show_register=True, reg_error='This username is already taken.')

        if selected_role not in ('trekker', 'client', 'guide'):
            selected_role = 'trekker'

        new_account = UserAccount(
            username=username,
            user_role=selected_role,
            is_verified=(selected_role in ('trekker', 'client')),
            is_enabled=True
        )
        new_account.set_password(password)

        db.session.add(new_account)
        db.session.commit()

        if selected_role == 'guide':
            success_msg = 'Registration successful! Your guide account is awaiting manager verification.'
        else:
            success_msg = 'Registration successful! You can now log in.'

        return render_template('login_page.html', success_message=success_msg)

    return render_template('login_page.html', show_register=True)


@client_controller.route('/dashboard')
def explorer_dashboard():
    """
    Trekker/Client explorer panel: shows open expeditions with optional search
    and displays the logged-in trekker's existing reservations.
    """
    if not _is_client_logged_in():
        return redirect('/portal/login')

    search_query = request.args.get('q', '').strip()
    query = Expedition.query.filter_by(expedition_status='Open')
    
    if search_query:
        query = query.filter(Expedition.title.ilike(f'%{search_query}%'))

    available_expeditions = query.all()
    user_reservations = TrekBooking.query.filter_by(trekker_id=session['user_id']).all()
    reserved_exp_ids = [booking.expedition_id for booking in user_reservations]

    return render_template(
        'explorer_panel.html',
        expeditions=available_expeditions,
        my_bookings=user_reservations,
        search_query=search_query,
        reserved_ids=reserved_exp_ids
    )


@client_controller.route('/book/<int:exp_id>', methods=['POST'])
def reserve_expedition(exp_id: int):
    """
    Books an available seat on the specified expedition for the logged-in trekker.
    """
    if not _is_client_logged_in():
        return redirect('/portal/login')

    expedition = Expedition.query.get(exp_id)
    if expedition and expedition.open_slots_valid():
        expedition.available_seats -= 1
        new_booking = TrekBooking(
            trekker_id=session['user_id'],
            expedition_id=exp_id
        )
        db.session.add(new_booking)
        db.session.commit()

    return redirect('/portal/dashboard')


# Helper method added dynamically to check slots safely
def _open_slots_valid(self):
    return self.expedition_status == 'Open' and self.available_seats > 0

Expedition.open_slots_valid = _open_slots_valid


@client_controller.route('/logout')
def handle_logout():
    """Terminates session and returns user to login portal."""
    session.clear()
    return redirect('/portal/login')
