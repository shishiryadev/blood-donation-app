from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from models import User, DonorProfile, RecipientRequest, DonationMatch, BloodDrive, DriveRegistration
from routes.auth import auth_bp
from routes.donors import donors_bp
from routes.recipients import recipients_bp
from routes.drives import drives_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(donors_bp, url_prefix="/api/donors")
    app.register_blueprint(recipients_bp, url_prefix="/api/recipients")
    app.register_blueprint(drives_bp, url_prefix="/api/drives")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})
    return app

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("send_alert")
def handle_send_alert(data):
    emit("receive_alert", data, broadcast=True)

@socketio.on("match_notify")
def handle_match_notify(data):
    uid = data.get("user_id")
    if uid:
        emit("match_notification", data, room=str(uid))
    else:
        emit("match_notification", data, broadcast=True)

@socketio.on("join")
def on_join(data):
    uid = str(data.get("user_id"))
    if uid:
        from flask_socketio import join_room
        join_room(uid)
        emit("joined", {"room": uid})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
