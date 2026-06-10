from __future__ import annotations

import os
import sqlite3
import uuid
from contextlib import closing
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from pixelpostii.models.post import (
    create_post,
    get_latest_published,
    get_post_by_slug,
    get_prev_next,
    init_db,
)

_ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("PIXELPOSTII_SECRET", "dev-secret-change-me")
    app.config["PASSWORD"] = os.environ.get("PIXELPOSTII_PASSWORD", "darkroom")

    base_dir = Path(__file__).parent
    app.config["DB_PATH"] = str(base_dir / "photoblog.db")
    app.config["UPLOAD_FOLDER"] = str(base_dir / "uploads")

    if config:
        app.config.update(config)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    init_db(app.config["DB_PATH"])

    # --- helpers -----------------------------------------------------------

    def get_db() -> sqlite3.Connection:
        conn = sqlite3.connect(app.config["DB_PATH"])
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def login_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get("logged_in"):
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated

    # --- routes ------------------------------------------------------------

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            if request.form.get("password") == app.config["PASSWORD"]:
                session["logged_in"] = True
                return redirect(url_for("index"))
            error = "Incorrect password."
        return render_template("login.html", error=error)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    @app.route("/")
    def index():
        with closing(get_db()) as conn:
            post = get_latest_published(conn)
            prev_post = next_post = None
            if post and post.published_at:
                prev_post, next_post = get_prev_next(conn, post.published_at)
        return render_template("post.html", post=post, prev_post=prev_post, next_post=next_post)

    @app.route("/post/<slug>")
    def view_post(slug):
        with closing(get_db()) as conn:
            post = get_post_by_slug(conn, slug)
            if post is None or post.status != "published":
                abort(404)
            prev_post, next_post = get_prev_next(conn, post.published_at)
        return render_template("post.html", post=post, prev_post=prev_post, next_post=next_post)

    @app.route("/new", methods=["GET", "POST"])
    @login_required
    def new_post():
        error = None
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            body = request.form.get("body", "").strip()
            action = request.form.get("action", "publish")
            image_file = request.files.get("image")

            if not title:
                error = "Title is required."
            elif not image_file or not image_file.filename:
                error = "An image is required."
            else:
                ext = Path(image_file.filename).suffix.lower()
                if ext not in _ALLOWED_EXTENSIONS:
                    error = f"File type {ext!r} is not allowed."
                else:
                    filename = f"{uuid.uuid4().hex}{ext}"
                    save_path = Path(app.config["UPLOAD_FOLDER"]) / filename
                    image_file.save(str(save_path))
                    status = "published" if action == "publish" else "draft"
                    with closing(get_db()) as conn:
                        create_post(conn, title, body, filename, status)
                    return redirect(url_for("index"))

        return render_template("new.html", error=error)

    @app.route("/uploads/<filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return app


def main() -> None:
    app = create_app()
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, port=port)


if __name__ == "__main__":
    main()
