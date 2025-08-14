from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, DonorProfile
from database import db
from . import auth_bp

@auth_bp.post("/register")
def register():
    data = request.get_json()
    required = ["name", "email", "password", "blood_type", "is_donor"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=data["email"].lower()).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        name=data["name"].strip(),
        email=data["email"].lower().strip(),
        password_hash=generate_password_hash(data["password"]),
        blood_type=data["blood_type"].upper().strip(),
        is_donor=bool(data["is_donor"]),
        phone=data.get("phone"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )
    db.session.add(user)
    db.session.flush()

    if user.is_donor:
        dp = DonorProfile(user_id=user.id, availability=True)
        db.session.add(dp)

    db.session.commit()
    token = create_access_token(identity=user.id)
    return jsonify({"message": "registered", "token": token, "user_id": user.id})

@auth_bp.post("/login")
def login():
    data = request.get_json()
    email = (data.get("email") or "").lower().strip()
    password = data.get("password") or ""
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity=user.id)
    return jsonify({"message": "ok", "token": token, "user": {
        "id": user.id, "name": user.name, "is_donor": user.is_donor, "blood_type": user.blood_type
    }})

@auth_bp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    u = User.query.get(uid)
    return jsonify({
        "id": u.id, "name": u.name, "email": u.email, "blood_type": u.blood_type,
        "is_donor": u.is_donor, "phone": u.phone, "latitude": u.latitude, "longitude": u.longitude
    })

@auth_bp.put("/me")
@jwt_required()
def update_me():
    uid = get_jwt_identity()
    u = User.query.get_or_404(uid)
    data = request.get_json()
    for f in ["name", "phone", "blood_type", "latitude", "longitude"]:
        if f in data:
            setattr(u, f, data[f])
    db.session.commit()
    return jsonify({"message": "updated"})
