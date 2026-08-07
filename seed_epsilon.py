import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from run_app import build_application
from database.models import db, UserAccount, Expedition, TrekBooking

def seed_database():
    """
    Populates the SQLite database with default demo credentials and sample Alpine expeditions.
    """
    app = build_application()
    with app.app_context():
        db.create_all()

        # 1. Seed Manager Account
        manager_user = UserAccount.query.filter_by(username='manager').first()
        if not manager_user:
            manager_user = UserAccount(
                username='manager',
                user_role='manager',
                is_verified=True,
                is_enabled=True
            )
            manager_user.set_password('manager')
            db.session.add(manager_user)

        # 2. Seed Client/Trekker Account
        client_user = UserAccount.query.filter_by(username='alice_client').first()
        if not client_user:
            client_user = UserAccount(
                username='alice_client',
                user_role='trekker',
                is_verified=True,
                is_enabled=True
            )
            client_user.set_password('password123')
            db.session.add(client_user)

        # 3. Seed Guide Account
        guide_user = UserAccount.query.filter_by(username='charlie_guide').first()
        if not guide_user:
            guide_user = UserAccount(
                username='charlie_guide',
                user_role='guide',
                is_verified=True,
                is_enabled=True
            )
            guide_user.set_password('password123')
            db.session.add(guide_user)

        db.session.commit()

        # Re-fetch ids after commit
        guide_id = guide_user.user_id if guide_user else None
        client_user = UserAccount.query.filter_by(username='alice_client').first()

        # 4. Seed Sample Expeditions (add each by title if missing)
        now = datetime.utcnow()
        sample_expeditions = [
            {
                "title": "Everest Base Camp Alpine Trail",
                "zone": "Himalayas, Nepal",
                "difficulty_grade": "Challenging",
                "max_participants": 12,
                "available_seats": 12,
                "start_date": now + timedelta(days=30),
                "end_date": now + timedelta(days=45),
                "lead_guide_id": guide_id,
            },
            {
                "title": "Patagonia Fitz Roy Traverse",
                "zone": "Andes, Argentina",
                "difficulty_grade": "Advanced",
                "max_participants": 10,
                "available_seats": 9,
                "start_date": now + timedelta(days=20),
                "end_date": now + timedelta(days=30),
                "lead_guide_id": guide_id,
            },
            {
                "title": "Mont Blanc Circuit Expedition",
                "zone": "Alps, France/Italy",
                "difficulty_grade": "Moderate",
                "max_participants": 15,
                "available_seats": 15,
                "start_date": now + timedelta(days=15),
                "end_date": now + timedelta(days=25),
                "lead_guide_id": guide_id,
            },
            {
                "title": "Kilimanjaro Uhuru Peak Ascent",
                "zone": "Tanzania, Africa",
                "difficulty_grade": "High Altitude / Moderate",
                "max_participants": 14,
                "available_seats": 14,
                "start_date": now + timedelta(days=60),
                "end_date": now + timedelta(days=68),
                "lead_guide_id": None,
            },
        ]

        added_count = 0
        for exp_data in sample_expeditions:
            if Expedition.query.filter_by(title=exp_data["title"]).first():
                continue
            db.session.add(Expedition(expedition_status='Open', **exp_data))
            added_count += 1

        if added_count:
            db.session.commit()

        # Book 1 seat for alice_client on Patagonia if not already booked
        patagonia = Expedition.query.filter_by(title="Patagonia Fitz Roy Traverse").first()
        if patagonia and client_user:
            existing_booking = TrekBooking.query.filter_by(
                trekker_id=client_user.user_id,
                expedition_id=patagonia.expedition_id,
            ).first()
            if not existing_booking:
                db.session.add(TrekBooking(
                    trekker_id=client_user.user_id,
                    expedition_id=patagonia.expedition_id,
                ))
                db.session.commit()

        print("================================================================")
        print("  PROJECT EPSILON 3 — DATABASE SEEDED SUCCESSFULLY              ")
        print("================================================================")
        print("  Demo Credentials:")
        print("    • Manager : manager / manager")
        print("    • Guide   : charlie_guide / password123")
        print("    • Trekker : alice_client / password123")
        print("================================================================")

if __name__ == '__main__':
    seed_database()
