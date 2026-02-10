from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import text

from config import Config
from models import db, User

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # DB init
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Auth init
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    # -------- Routes --------

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            welcome_message=app.config["WELCOME_MESSAGE"],
        )

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""

            if len(username) < 3:
                flash("Логин должен быть минимум 3 символа.", "error")
                return redirect(url_for("register"))
            if len(password) < 6:
                flash("Пароль должен быть минимум 6 символов.", "error")
                return redirect(url_for("register"))

            if User.query.filter_by(username=username).first():
                flash("Такой логин уже существует.", "error")
                return redirect(url_for("register"))

            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash("Аккаунт создан. Теперь войдите.", "success")
            return redirect(url_for("login"))

        return render_template("register.html", register_title=app.config["REGISTER_TITLE"])

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""

            user = User.query.filter_by(username=username).first()
            if not user or not user.check_password(password):
                flash("Неверный логин или пароль.", "error")
                return redirect(url_for("login"))

            if user.status != "active":
                flash(f"Вход запрещён. Статус пользователя: {user.status}", "error")
                return redirect(url_for("login"))

            login_user(user)
            return redirect(url_for("profile"))

        return render_template("login.html", login_title=app.config["LOGIN_TITLE"])

    @app.post("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.get("/profile")
    @login_required
    def profile():
        return render_template("profile.html", user=current_user)

    # ---- Health checks (for k8s probes) ----
    @app.get("/health/live")
    def health_live():
        return {"status": "ok"}, 200

    @app.get("/health/ready")
    def health_ready():
        # readiness = can we reach the DB?
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ready"}, 200
        except Exception:
            return {"status": "not_ready"}, 503

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
