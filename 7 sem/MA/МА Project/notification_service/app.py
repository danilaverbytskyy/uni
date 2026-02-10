from flask import Flask, jsonify, request, render_template
from sqlalchemy import text

from config import Config
from models import db, Notification
from common.jwt_auth import decode_token, get_bearer_token

def require_user():
    token = get_bearer_token(request.headers.get("Authorization"))
    if not token:
        return None, ({"error": "missing bearer token"}, 401)
    try:
        payload = decode_token(token)
        return payload, None
    except Exception:
        return None, ({"error": "invalid token"}, 401)

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/")
    def ui_index():
        return render_template("index.html")


    @app.post("/api/notify")
    def send_notification():
        payload, err = require_user()
        if err:
            return err
        user_id = int(payload["sub"])
        username = payload.get("username") or ""

        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()
        if not message:
            return jsonify({"error": "message required"}), 400

        n = Notification(user_id=user_id, username=username, message=message)
        db.session.add(n)
        db.session.commit()

        print(f"[notification-service] notify user={username}({user_id}): {message}")

        return jsonify({"ok": True, "id": n.id}), 201

    @app.get("/api/notifications")
    def list_notifications():
        payload, err = require_user()
        if err:
            return err
        user_id = int(payload["sub"])

        items = (
            Notification.query
            .filter_by(user_id=user_id)
            .order_by(Notification.created_at.desc())
            .limit(50)
            .all()
        )
        return jsonify([
            {
                "id": n.id,
                "message": n.message,
                "created_at": n.created_at.isoformat() + "Z",
            } for n in items
        ]), 200

    @app.get("/health/live")
    def health_live():
        return {"status": "ok"}, 200

    @app.get("/health/ready")
    def health_ready():
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ready"}, 200
        except Exception:
            return {"status": "not_ready"}, 503

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
