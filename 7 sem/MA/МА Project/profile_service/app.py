from flask import Flask, jsonify, request, render_template
from sqlalchemy import text

from config import Config
from models import db, Profile
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


    @app.get("/api/profile")
    def get_profile():
        payload, err = require_user()
        if err:
            return err
        user_id = int(payload["sub"])
        username = payload.get("username") or ""

        p = Profile.query.filter_by(user_id=user_id).first()
        if not p:
            p = Profile(user_id=user_id, username=username)
            db.session.add(p)
            db.session.commit()

        return jsonify({
            "user_id": p.user_id,
            "username": p.username,
            "full_name": p.full_name,
            "email": p.email,
            "bio": p.bio,
        }), 200

    @app.put("/api/profile")
    def update_profile():
        payload, err = require_user()
        if err:
            return err
        user_id = int(payload["sub"])
        username = payload.get("username") or ""

        data = request.get_json(silent=True) or {}
        p = Profile.query.filter_by(user_id=user_id).first()
        if not p:
            p = Profile(user_id=user_id, username=username)
            db.session.add(p)

        p.full_name = data.get("full_name", p.full_name)
        p.email = data.get("email", p.email)
        p.bio = data.get("bio", p.bio)
        db.session.commit()

        return jsonify({"ok": True}), 200

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
