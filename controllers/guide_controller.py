from flask import Blueprint, render_template, request, redirect, session
from database.models import db, Expedition

guide_controller = Blueprint('guide_controller', __name__, url_prefix='/staff')


def _is_guide_logged_in() -> bool:
    """Helper to verify if the active session belongs to a verified expedition guide."""
    return session.get('user_role') == 'guide' and 'user_id' in session


@guide_controller.route('/dashboard')
def leader_dashboard():
    """
    Expedition Leader Panel: Displays expeditions assigned to the logged-in guide.
    """
    if not _is_guide_logged_in():
        return redirect('/portal/login')

    assigned_expeditions = Expedition.query.filter_by(lead_guide_id=session['user_id']).all()
    return render_template('leader_panel.html', expeditions=assigned_expeditions)


@guide_controller.route('/update/<int:exp_id>', methods=['POST'])
def update_expedition_status(exp_id: int):
    """
    Allows the assigned guide to adjust status and available seat count for an expedition.
    """
    if not _is_guide_logged_in():
        return redirect('/portal/login')

    expedition = Expedition.query.get(exp_id)
    if expedition and expedition.lead_guide_id == session['user_id']:
        new_status = request.form.get('status', expedition.expedition_status)
        try:
            new_seats = int(request.form.get('seats', expedition.available_seats))
            if 0 <= new_seats <= expedition.max_participants:
                expedition.available_seats = new_seats
        except (ValueError, TypeError):
            pass

        if new_status in ('Open', 'Closed', 'Completed'):
            expedition.expedition_status = new_status

        db.session.commit()

    return redirect('/staff/dashboard')
