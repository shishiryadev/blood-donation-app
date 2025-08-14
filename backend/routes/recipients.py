from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from math import radians, sin, cos, asin, sqrt
from models import User, RecipientRequest
from database import db
from . import recipients_bp

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians((lat2 or 0) - (lat1 or 0))
    dlon = radians((lon2 or 0) - (lon1 or 0))
    a = sin(dlat/2)**2 + cos(radians(lat1 or 0)) * cos(radians(lat2 or 0)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

@recipients_bp.post("/request")
@jwt_required()
def create_request():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    required = ["blood_type_needed", "units_needed", "latitude", "longitude"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400
    rr = RecipientRequest(
        requester_id=uid,
        blood_type_needed=data["blood_type_needed"].upper(),
        units_needed=int(data["units_needed"]),
        urgency=data.get("urgency", "normal"),
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        active=True
    )
    db.session.add(rr)
    db.session.commit()
    return jsonify({"message": "created", "request_id": rr.id})

@recipients_bp.get("/nearby_donors")
@jwt_required()
def nearby_donors():
    bt = request.args.get("blood_type")
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    max_km = float(request.args.get("max_km") or 50)
    from models import User, DonorProfile
    q = User.query.filter_by(is_donor=True).join(DonorProfile, isouter=True)
    if bt:
        q = q.filter(User.blood_type == bt.upper())
    results = []
    for d in q.all():
        if d.latitude is None or d.longitude is None or lat is None or lon is None:
            continue
        dist = haversine(lat, lon, d.latitude, d.longitude)
        if dist <= max_km:
            results.append({
                "id": d.id, "name": d.name, "blood_type": d.blood_type,
                "phone": d.phone, "distance_km": round(dist, 2)
            })
    results.sort(key=lambda x: x["distance_km"])
    return jsonify(results)

@recipients_bp.get("/requests")
@jwt_required()
def my_requests():
    uid = get_jwt_identity()
    data = [
        {
            "id": r.id,
            "blood_type_needed": r.blood_type_needed,
            "units_needed": r.units_needed,
            "active": r.active,
            "created_at": r.created_at.isoformat()
        }
        for r in RecipientRequest.query.filter_by(requester_id=uid)
        .order_by(RecipientRequest.created_at.desc()).all()
    ]
    return jsonify(data)

@recipients_bp.post("/close")
@jwt_required()
def close_request():
    uid = get_jwt_identity()
    rid = (request.get_json() or {}).get("request_id")
    r = RecipientRequest.query.get_or_404(rid)
    if r.requester_id != uid:
        return jsonify({"error": "Not owner"}), 403
    r.active = False
    db.session.commit()
    return jsonify({"message": "closed"})
