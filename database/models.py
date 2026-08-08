from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# Initialize SQLAlchemy DB instance 
db = SQLAlchemy()

class UserAccount(db.Model):
    """
    Represents a registered user within the Project Epsilon 3 ecosystem.
    Roles include: 'trekker' (client), 'guide' (expedition staff), and 'manager' (admin).
    """
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(30), default='trekker', nullable=False)
    is_verified = db.Column(db.Boolean, default=True, nullable=False)
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, plain_text: str) -> None:
        """Hashes and stores the password securely using PBKDF2-SHA256."""
        self.password_hash = generate_password_hash(plain_text, method='pbkdf2:sha256')

    def check_password(self, plain_text: str) -> bool:
        """Verifies a plaintext password against the stored secure hash."""
        return check_password_hash(self.password_hash, plain_text)

    # if not used it would just show the memory location of instead of the attributes that are taken as input
    def __repr__(self) -> str:
        return f"<UserAccount id={self.user_id} username='{self.username}' role='{self.user_role}'>"


class Expedition(db.Model):
    """
    Represents a trekking expedition available for booking or management.
    Status lifecycle: 'Pending Approval' -> 'Open' -> 'Closed' or 'Completed'.
    """
    __tablename__ = 'expeditions'

    expedition_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    zone = db.Column(db.String(100), nullable=False)
    difficulty_grade = db.Column(db.String(50), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    expedition_status = db.Column(db.String(50), default='Pending Approval', nullable=False)
    lead_guide_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)


    # backref creates a 2 sided relation btw both the tables 
    # lazy loading is simply like async await 
    
    guide = db.relationship(
        'UserAccount',
        backref=db.backref('assigned_expeditions', lazy=True),
        foreign_keys=[lead_guide_id]
    )

    def __repr__(self) -> str:
        return f"<Expedition id={self.expedition_id} title='{self.title}' status='{self.expedition_status}'>"


class TrekBooking(db.Model):
    """
    Represents an active reservation made by a trekker for a specific expedition.
    """
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True)
    trekker_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    expedition_id = db.Column(db.Integer, db.ForeignKey('expeditions.expedition_id', ondelete='CASCADE'), nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    trekker = db.relationship(
        'UserAccount',
        backref=db.backref('bookings', cascade='all, delete-orphan', lazy=True),
        foreign_keys=[trekker_id]
    )
    expedition = db.relationship(
        'Expedition',
        backref=db.backref('bookings', cascade='all, delete-orphan', lazy=True)
    )

    def __repr__(self) -> str:
        return f"<TrekBooking id={self.booking_id} trekker_id={self.trekker_id} exp_id={self.expedition_id}>"
