from datetime import datetime
from database import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    phone = db.Column(db.String(30))
    is_donor = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donor_profile = db.relationship("DonorProfile", backref="user", uselist=False)

class DonorProfile(db.Model):
    __tablename__ = "donor_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    last_donation = db.Column(db.Date)
    availability = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

class RecipientRequest(db.Model):
    __tablename__ = "recipient_requests"
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    blood_type_needed = db.Column(db.String(5), nullable=False)
    units_needed = db.Column(db.Integer, default=1)
    urgency = db.Column(db.String(20), default="normal")
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DonationMatch(db.Model):
    __tablename__ = "donation_matches"
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("recipient_requests.id"))
    donor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BloodDrive(db.Model):
    __tablename__ = "blood_drives"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    location_name = db.Column(db.String(180), nullable=False)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DriveRegistration(db.Model):
    __tablename__ = "drive_registrations"
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey("blood_drives.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(30), default="donor")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
