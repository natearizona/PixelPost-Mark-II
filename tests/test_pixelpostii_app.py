"""
PixelPost II — Milestone B prototype tests.

Covers the nine-step publish flow:
  start → login → upload → title/body → publish → persist → view → navigate
"""
import io
import pytest
from pixelpostii.app import create_app


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def app(tmp_path):
    return create_app({
        "TESTING": True,
        "DB_PATH": str(tmp_path / "test.db"),
        "UPLOAD_FOLDER": str(tmp_path / "uploads"),
        "SECRET_KEY": "test-secret",
        "PASSWORD": "darkroom",
    })


@pytest.fixture
def client(app):
    return app.test_client()


def _login(client):
    return client.post("/login", data={"password": "darkroom"}, follow_redirects=True)


def _fake_image(name: str = "test.jpg") -> tuple:
    """Minimal JPEG header bytes — enough to satisfy file save."""
    data = b"\xff\xd8\xff\xe0" + b"\x00" * 16
    return (io.BytesIO(data), name)


def _publish(client, title: str, body: str = "") -> None:
    client.post(
        "/new",
        data={"title": title, "body": body, "action": "publish", "image": _fake_image()},
        content_type="multipart/form-data",
    )


# ── authentication ────────────────────────────────────────────────────────────

def test_login_required_for_new(client):
    r = client.get("/new")
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_login_wrong_password(client):
    r = client.post("/login", data={"password": "wrong"})
    assert r.status_code == 200
    assert b"Incorrect password" in r.data


def test_login_success(client):
    r = _login(client)
    assert r.status_code == 200
    assert b"New" in r.data


def test_logout_clears_session(client):
    _login(client)
    client.get("/logout")
    r = client.get("/new")
    assert r.status_code == 302


# ── empty state ───────────────────────────────────────────────────────────────

def test_index_empty_state(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"No photographs published yet" in r.data


# ── publish flow ──────────────────────────────────────────────────────────────

def test_publish_post_redirects_to_index(client):
    _login(client)
    r = client.post(
        "/new",
        data={"title": "Red Rock Morning", "body": "First light.", "action": "publish",
              "image": _fake_image()},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Red Rock Morning" in r.data


def test_published_post_visible_on_index(client):
    _login(client)
    _publish(client, "Desert Light")
    r = client.get("/")
    assert b"Desert Light" in r.data


def test_draft_not_visible_on_index(client):
    _login(client)
    client.post(
        "/new",
        data={"title": "Hidden Draft", "body": "", "action": "draft", "image": _fake_image()},
        content_type="multipart/form-data",
    )
    r = client.get("/")
    assert b"Hidden Draft" not in r.data


def test_post_requires_title(client):
    _login(client)
    r = client.post(
        "/new",
        data={"title": "", "body": "no title", "action": "publish", "image": _fake_image()},
        content_type="multipart/form-data",
    )
    assert b"Title is required" in r.data


def test_post_requires_image(client):
    _login(client)
    r = client.post(
        "/new",
        data={"title": "No Image", "body": "", "action": "publish"},
        content_type="multipart/form-data",
    )
    assert b"image is required" in r.data


def test_disallowed_file_type_rejected(client):
    _login(client)
    r = client.post(
        "/new",
        data={"title": "Bad File", "body": "", "action": "publish",
              "image": (io.BytesIO(b"data"), "virus.exe")},
        content_type="multipart/form-data",
    )
    assert b"not allowed" in r.data


# ── slug and single-post view ─────────────────────────────────────────────────

def test_post_accessible_by_slug(client):
    _login(client)
    _publish(client, "Canyon Walls")
    r = client.get("/post/canyon-walls")
    assert r.status_code == 200
    assert b"Canyon Walls" in r.data


def test_unknown_slug_returns_404(client):
    r = client.get("/post/does-not-exist")
    assert r.status_code == 404


def test_draft_slug_returns_404(client):
    _login(client)
    client.post(
        "/new",
        data={"title": "Secret Draft", "body": "", "action": "draft", "image": _fake_image()},
        content_type="multipart/form-data",
    )
    r = client.get("/post/secret-draft")
    assert r.status_code == 404


def test_slug_generated_from_title(client):
    _login(client)
    _publish(client, "Blue Hour Over Zion")
    r = client.get("/post/blue-hour-over-zion")
    assert r.status_code == 200


def test_duplicate_title_gets_unique_slug(client):
    _login(client)
    _publish(client, "Morning Light")
    _publish(client, "Morning Light")
    r1 = client.get("/post/morning-light")
    r2 = client.get("/post/morning-light-1")
    assert r1.status_code == 200
    assert r2.status_code == 200


# ── chronological navigation ──────────────────────────────────────────────────

def test_index_shows_latest_post(client):
    _login(client)
    _publish(client, "First")
    _publish(client, "Second")
    _publish(client, "Third")
    r = client.get("/")
    assert b"Third" in r.data


def test_prev_link_present_on_later_post(client):
    _login(client)
    _publish(client, "Earlier")
    _publish(client, "Later")
    r = client.get("/")
    assert b"Earlier" in r.data  # prev link


def test_next_link_present_on_earlier_post(client):
    _login(client)
    _publish(client, "Alpha")
    _publish(client, "Beta")
    r = client.get("/post/alpha")
    assert b"Beta" in r.data  # next link
