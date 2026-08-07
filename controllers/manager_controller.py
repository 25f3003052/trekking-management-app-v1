from datetime import datetime
from flask import Blueprint, render_template, request, redirect, session
from database.models import db, UserAccount, Expedition

manager_controller = Blueprint('manager_controller', __name__, url_prefix='/admin')


def _is_manager_logged_in() -> bool:
    """Verifies that the session user has 'manager' admin privileges."""
    return session.get('user_role') == 'manager' and 'user_id' in session


@manager_controller.route('/dashboard')
def admin_dashboard():
    """
    Manager Console: Displays all expeditions, guide roster, trekker roster,
    and controls for expedition creation and account verification/suspension.
    """
    if not _is_manager_logged_in():
        return redirect('/portal/login')

    all_expeditions = Expedition.query.all()
    guides = UserAccount.query.filter_by(user_role='guide').all()
    trekkers = UserAccount.query.filter(UserAccount.user_role.in_(['trekker', 'client'])).all()

    return render_template(
        'admin_panel.html',
        expeditions=all_expeditions,
        guides=guides,
        trekkers=trekkers
    )


@manager_controller.route('/create_expedition', methods=['POST'])
def create_new_expedition():
    """
    Creates a new trekking expedition and optionally assigns an approved guide.
    """
    if not _is_manager_logged_in():
        return redirect('/portal/login')

    title = request.form.get('title', '').strip()
    zone = request.form.get('zone', '').strip()
    difficulty = request.form.get('difficulty', '').strip()

    try:
        max_cap = int(request.form.get('max_participants', 10))
        d1 = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        d2 = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    except (ValueError, TypeError):
        return redirect('/admin/dashboard')

    guide_id_raw = request.form.get('lead_guide_id')
    assigned_guide_id = int(guide_id_raw) if guide_id_raw and guide_id_raw.isdigit() else None

    new_expedition = Expedition(
        title=title,
        zone=zone,
        difficulty_grade=difficulty,
        max_participants=max_cap,
        available_seats=max_cap,
        start_date=d1,
        end_date=d2,
        lead_guide_id=assigned_guide_id,
        expedition_status='Open'
    )
    db.session.add(new_expedition)
    db.session.commit()

    return redirect('/admin/dashboard')


@manager_controller.route('/verify/<int:account_id>', methods=['POST'])
def verify_guide_account(account_id: int):
    """
    Approves a pending guide account so they can log in and manage expeditions.
    """
    if not _is_manager_logged_in():
        return redirect('/portal/login')

    target_account = UserAccount.query.get(account_id)
    if target_account and target_account.user_role == 'guide':
        target_account.is_verified = True
        db.session.commit()

    return redirect('/admin/dashboard')


@manager_controller.route('/suspend/<int:account_id>', methods=['POST'])
def suspend_account(account_id: int):
    """
    Suspends/bans a guide or trekker account, preventing login access.
    """
    if not _is_manager_logged_in():
        return redirect('/portal/login')

    target_account = UserAccount.query.get(account_id)
    if target_account and target_account.user_role != 'manager':
        target_account.is_enabled = False
        db.session.commit()

    return redirect('/admin/dashboard')
