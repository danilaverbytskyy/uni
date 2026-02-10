from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import json
import urllib.request
import urllib.error
from sqlalchemy import text

from config import Config
from models import db, User
from common.jwt_auth import create_access_token, decode_token, get_bearer_token

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            welcome_message=app.config["WELCOME_MESSAGE"],
        )

    @app.route("/register", methods=["GET", "POST"])
    def register_page():
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""

            if len(username) < 3 or len(password) < 6:
                flash("Логин >= 3 символа, пароль >= 6 символов.", "error")
                return redirect(url_for("register_page"))

            if User.query.filter_by(username=username).first():
                flash("Такой логин уже существует.", "error")
                return redirect(url_for("register_page"))

            u = User(username=username)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            flash("Аккаунт создан. Теперь войдите.", "success")
            return redirect(url_for("login_page"))

        return render_template("register.html", register_title=app.config["REGISTER_TITLE"])

    @app.route("/login", methods=["GET", "POST"])
    def login_page():
        token = None
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""

            u = User.query.filter_by(username=username).first()
            if not u or not u.check_password(password):
                flash("Неверный логин или пароль.", "error")
                return redirect(url_for("login_page"))

            token = create_access_token({"sub": str(u.id), "username": u.username})
            flash("Успешный вход. Токен сгенерирован.", "success")

        return render_template("login.html", login_title=app.config["LOGIN_TITLE"], token=token)


    @app.get("/me")
    def me_page():
        return render_template("me.html")

    def _proxy_profile_service(method: str, token: str, body=None):
        base_url = app.config.get("PROFILE_SERVICE_URL", "http://profile-service:5000")
        url = base_url.rstrip("/") + "/api/profile"

        headers = {"Authorization": f"Bearer {token}"}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read().decode("utf-8")
                return resp.getcode(), raw
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8")
            return e.code, raw
        except Exception:
            return 503, json.dumps({"error": "profile service unavailable"})

    @app.route("/api/me/profile", methods=["GET", "PUT"])
    def api_me_profile():
        token = get_bearer_token(request.headers.get("Authorization"))
        if not token:
            return jsonify({"error": "missing bearer token"}), 401

        if request.method == "GET":
            status, raw = _proxy_profile_service("GET", token)
        else:
            body = request.get_json(silent=True) or {}
            status, raw = _proxy_profile_service("PUT", token, body=body)

        return raw, status, {"Content-Type": "application/json"}

    @app.post("/api/register")
    def api_register():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        if len(username) < 3 or len(password) < 6:
            return jsonify({"error": "username>=3 and password>=6 required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "username already exists"}), 409

        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return jsonify({"id": u.id, "username": u.username}), 201

    @app.post("/api/login")
    def api_login():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        u = User.query.filter_by(username=username).first()
        if not u or not u.check_password(password):
            return jsonify({"error": "invalid credentials"}), 401

        token = create_access_token({"sub": str(u.id), "username": u.username})
        return jsonify({"access_token": token, "token_type": "Bearer"}), 200

    @app.get("/api/validate")
    def api_validate():
        token = get_bearer_token(request.headers.get("Authorization"))
        if not token:
            return jsonify({"error": "missing bearer token"}), 401
        try:
            payload = decode_token(token)
            return jsonify({"ok": True, "user": {"id": payload.get("sub"), "username": payload.get("username")}}), 200
        except Exception:
            return jsonify({"ok": False, "error": "invalid token"}), 401

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
