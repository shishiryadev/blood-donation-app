from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import BloodDrive, DriveRegistration
from database import db
from . import drives_bp
from datetime import datetime

@drives_bp.post("/")
@jwt_required()
def create_drive():
    data = request.get_json() or {}
    required = ["title", "location_name", "start_time", "end_time"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400
    drive = BloodDrive(
        title=data["title"],
        location_name=data["location_name"],
        address=data.get("address"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        start_time=datetime.fromisoformat(data["start_time"]),
        end_time=datetime.fromisoformat(data["end_time"]),
        description=data.get("description")
    )
    db.session.add(drive)
    db.session.commit()
    return jsonify({"message": "created", "drive_id": drive.id})

@drives_bp.get("/")
def list_drives():
    drives = BloodDrive.query.order_by(BloodDrive.start_time.asc()).all()
    return jsonify([
        {
            "id": d.id,
            "title": d.title,
            "location_name": d.location_name,
            "address": d.address,
            "start_time": d.start_time.isoformat(),
            "end_time": d.end_time.isoformat(),
            "latitude": d.latitude,
            "longitude": d.longitude,
            "description": d.description
        }
        for d in drives
    ])

@drives_bp.post("/register")
@jwt_required()
def register_for_drive():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    drive_id = data.get("drive_id")
    role = (data.get("role") or "donor").lower()
    if not drive_id:
        return jsonify({"error": "drive_id required"}), 400
    reg = DriveRegistration(drive_id=drive_id, user_id=uid, role=role)
    db.session.add(reg)
    db.session.commit()
    return jsonify({"message": "registered"})
