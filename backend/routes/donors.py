from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from math import radians, sin, cos, asin, sqrt
from models import User, DonorProfile, RecipientRequest, DonationMatch
from database import db
from . import donors_bp

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # km
    dlat = radians((lat2 or 0) - (lat1 or 0))
    dlon = radians((lon2 or 0) - (lon1 or 0))
    a = sin(dlat/2)**2 + cos(radians(lat1 or 0)) * cos(radians(lat2 or 0)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

@donors_bp.get("/")
def list_donors():
    bt = request.args.get("blood_type")
    max_km = float(request.args.get("max_km") or 50)
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    q = User.query.filter_by(is_donor=True).join(DonorProfile, isouter=True)
    if bt:
        q = q.filter(User.blood_type == bt.upper())
    donors = []
    for d in q.all():
        if lat is not None and lon is not None and d.latitude is not None and d.longitude is not None:
            dist = haversine(lat, lon, d.latitude, d.longitude)
            if dist > max_km:
                continue
        else:
            dist = None
        donors.append({
            "id": d.id, "name": d.name, "blood_type": d.blood_type, "phone": d.phone,
            "lat": d.latitude, "lon": d.longitude, "distance_km": round(dist, 2) if dist is not None else None
        })
    return jsonify(donors)

@donors_bp.put("/profile")
@jwt_required()
def update_profile():
    uid = get_jwt_identity()
    u = User.query.get_or_404(uid)
    if not u.is_donor:
        return jsonify({"error": "Not a donor account"}), 403
    data = request.get_json() or {}
    dp = DonorProfile.query.filter_by(user_id=u.id).first()
    if not dp:
        dp = DonorProfile(user_id=u.id)
        db.session.add(dp)
    if "availability" in data:
        dp.availability = bool(data["availability"])
    if "last_donation" in data:
        dp.last_donation = data["last_donation"]
    if "notes" in data:
        dp.notes = data["notes"]
    db.session.commit()
    return jsonify({"message": "profile updated"})

@donors_bp.post("/accept_request")
@jwt_required()
def accept_request():
    uid = get_jwt_identity()
    donor = User.query.get_or_404(uid)
    if not donor.is_donor:
        return jsonify({"error": "Only donors can accept"}), 403
    req_id = (request.get_json() or {}).get("request_id")
    req = RecipientRequest.query.get_or_404(req_id)
    match = DonationMatch(request_id=req.id, donor_id=donor.id, status="accepted")
    db.session.add(match)
    db.session.commit()
    return jsonify({"message": "accepted", "match_id": match.id})
