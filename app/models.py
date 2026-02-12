from datetime import datetime
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash # Though request says password not required, hashing OTPs is required.
import hashlib

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    otp_hash = db.Column(db.String(128))
    otp_expiry = db.Column(db.DateTime)

    def set_otp(self, otp):
        self.otp_hash = hashlib.sha256(otp.encode()).hexdigest()

    def check_otp(self, otp):
        if self.otp_hash == hashlib.sha256(otp.encode()).hexdigest():
            return True
        return False

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.String(20), default='Pending') # Pending, In-Progress, Completed
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # nullable for potential anonymous actions if ever needed, but likely auth required
    action = db.Column(db.String(50), nullable=False) # Login, OTP Request, Task Created, etc.
    details = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))
