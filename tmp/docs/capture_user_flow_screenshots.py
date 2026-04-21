#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "tmp" / "docs" / "demo_state.json"
ASSET_ROOT = ROOT / "docs" / "product-user-flows" / "assets"
PWCLI = Path(os.environ.get("PWCLI", Path.home() / ".codex" / "skills" / "playwright" / "scripts" / "playwright_cli.sh"))
RUN_ID = str(int(time.time()))
INITIALIZED_SESSIONS: set[str] = set()
SESSION = f"{RUN_ID}-docs-run"


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def run(cmd: list[str], *, env: dict | None = None) -> subprocess.CompletedProcess:
    result = subprocess.run(cmd, cwd=ROOT, env=env, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
    return result


def pw(session: str, *args: str) -> str:
    cmd = [str(PWCLI), "--session", session, *args]
    result = run(cmd, env=os.environ.copy())
    return result.stdout


def js(session: str, script: str) -> str:
    return pw(session, "run-code", script)


def open_page(session: str, url: str) -> None:
    if session not in INITIALIZED_SESSIONS:
        pw(session, "open", url)
        INITIALIZED_SESSIONS.add(session)
    else:
        js(session, f"await page.goto({json.dumps(url)});")
    pw(session, "resize", "1440", "1100")
    time.sleep(0.5)


def take_shot(session: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    output = pw(session, "screenshot")
    match = re.search(r"\[Screenshot of viewport\]\(([^)]+\.png)\)", output)
    if not match:
        raise RuntimeError(f"Could not find screenshot path in Playwright output:\n{output}")
    source = ROOT / match.group(1)
    if not source.exists():
        raise FileNotFoundError(f"Expected screenshot file not found: {source}")
    shutil.copy2(source, path)


def doctor_cookie(token: str, base_url: str) -> dict:
    out = run(
        [
            str(ROOT / ".venv311" / "bin" / "python"),
            str(ROOT / "tmp" / "docs" / "create_doctor_session.py"),
            "--token",
            token,
            "--base-url",
            base_url,
        ]
    ).stdout
    return json.loads(out)


def set_cookie_and_goto(session: str, cookie: dict, url: str) -> None:
    open_page(session, cookie["url"])
    js(session, f"await context.addCookies([{json.dumps(cookie)}]);")
    js(session, f"await page.goto({json.dumps(url)});")
    time.sleep(0.7)


def clear_state(session: str, base_url: str) -> None:
    open_page(session, base_url)
    js(
        session,
        "\n".join(
            [
                "await context.clearCookies();",
                "await page.goto('about:blank');",
            ]
        ),
    )
    time.sleep(0.3)


def ensure_asset_dir(slug: str) -> Path:
    path = ASSET_ROOT / slug
    path.mkdir(parents=True, exist_ok=True)
    return path


def capture_overview(base_url: str) -> None:
    slug = "platform-overview-and-role-map"
    asset_dir = ensure_asset_dir(slug)
    session = SESSION
    open_page(session, f"{base_url}/")
    take_shot(session, asset_dir / "01-home-overview.png")


def capture_admin_partner(base_url: str, state: dict) -> None:
    slug = "admin-partner-provisioning-and-field-rep-upload"
    asset_dir = ensure_asset_dir(slug)
    session = SESSION
    clear_state(session, base_url)
    open_page(session, f"{base_url}/admin/access/")
    take_shot(session, asset_dir / "01-admin-access.png")

    js(
        session,
        "\n".join(
            [
                f"await page.fill('input[name=password]', {json.dumps(state['admin_access_password'])});",
                "await Promise.all([page.waitForLoadState('networkidle'), page.click('button[type=submit]')]);",
            ]
        ),
    )
    take_shot(session, asset_dir / "02-partner-create-form.png")

    partner_name = f"Docs Pack Partner {int(time.time())}"
    js(
        session,
        "\n".join(
            [
                f"await page.fill('input[name=partner_name]', {json.dumps(partner_name)});",
                f"await page.setInputFiles('input[name=csv_file]', {json.dumps(state['assets']['field_rep_csv'])});",
                "await Promise.all([page.waitForLoadState('networkidle'), page.click('button[type=submit]')]);",
            ]
        ),
    )
    take_shot(session, asset_dir / "03-partner-created.png")


def capture_doctor_registration(base_url: str, state: dict) -> None:
    session_self = SESSION
    slug_self = "doctor-self-registration-and-portal-access"
    asset_dir_self = ensure_asset_dir(slug_self)
    clear_state(session_self, base_url)
    open_page(session_self, f"{base_url}/doctor/register/")
    take_shot(session_self, asset_dir_self / "01-doctor-self-registration-form.png")

    self_cookie = doctor_cookie(state["self_doctor"]["portal_token"], base_url)
    set_cookie_and_goto(session_self, self_cookie, f"{base_url}/d/{state['self_doctor']['portal_token']}/")
    take_shot(session_self, asset_dir_self / "02-doctor-self-portal-home.png")

    session_partner = SESSION
    slug_partner = "partner-led-doctor-onboarding"
    asset_dir_partner = ensure_asset_dir(slug_partner)
    clear_state(session_partner, base_url)
    open_page(session_partner, f"{base_url}/doctor/register/{state['partner']['registration_token']}/")
    take_shot(session_partner, asset_dir_partner / "01-partner-led-registration-form.png")

    partner_cookie = doctor_cookie(state["partner_doctor"]["portal_token"], base_url)
    set_cookie_and_goto(session_partner, partner_cookie, f"{base_url}/d/{state['partner_doctor']['portal_token']}/")
    take_shot(session_partner, asset_dir_partner / "02-partner-doctor-portal-home.png")


def capture_doctor_portal(base_url: str, state: dict) -> None:
    slug_add = "doctor-portal-add-patient-and-share-link"
    slug_update = "doctor-portal-update-card-and-profile"
    asset_dir_add = ensure_asset_dir(slug_add)
    asset_dir_update = ensure_asset_dir(slug_update)
    session = SESSION
    cookie = doctor_cookie(state["self_doctor"]["portal_token"], base_url)
    clear_state(session, base_url)

    set_cookie_and_goto(session, cookie, f"{base_url}/d/{state['self_doctor']['portal_token']}/add/")
    take_shot(session, asset_dir_add / "01-doctor-add-patient-form.png")

    new_child_name = f"Portal Demo Child {int(time.time())}"
    js(
        session,
        "\n".join(
            [
                f"await page.fill('#id_child_name', {json.dumps(new_child_name)});",
                "await page.selectOption('#id_gender', 'F');",
                "await page.fill('#id_date_of_birth', '2025-11-20');",
                "await page.selectOption('#id_state', 'Karnataka');",
                f"await page.fill('#id_parent_whatsapp', {json.dumps(state['parents']['public']['whatsapp'])});",
                "await Promise.all([page.waitForLoadState('networkidle'), page.click('button[type=submit]')]);",
            ]
        ),
    )
    take_shot(session, asset_dir_add / "02-doctor-card-after-add.png")

    set_cookie_and_goto(session, cookie, f"{base_url}/d/{state['self_doctor']['portal_token']}/update/")
    take_shot(session, asset_dir_update / "01-doctor-update-lookup.png")

    js(
        session,
        "\n".join(
            [
                f"await page.fill('#id_parent_whatsapp', {json.dumps(state['parents']['public']['whatsapp'])});",
                "await Promise.all([page.waitForLoadState('networkidle'), page.click('button[type=submit]')]);",
            ]
        ),
    )
    take_shot(session, asset_dir_update / "02-doctor-select-child.png")

    set_cookie_and_goto(
        session,
        cookie,
        f"{base_url}/d/{state['self_doctor']['portal_token']}/card/{state['children']['primary']['id']}/",
    )
    take_shot(session, asset_dir_update / "03-doctor-vaccination-card.png")

    set_cookie_and_goto(
        session,
        cookie,
        f"{base_url}/d/{state['self_doctor']['portal_token']}/profile/",
    )
    take_shot(session, asset_dir_update / "04-doctor-profile.png")


def capture_reminders_and_education(base_url: str, state: dict) -> None:
    slug = "reminders-and-education-workflows"
    asset_dir = ensure_asset_dir(slug)
    session = SESSION
    cookie = doctor_cookie(state["self_doctor"]["portal_token"], base_url)
    clear_state(session, base_url)

    set_cookie_and_goto(session, cookie, f"{base_url}/d/{state['self_doctor']['portal_token']}/reminders/")
    take_shot(session, asset_dir / "01-reminders-dashboard.png")

    set_cookie_and_goto(
        session,
        cookie,
        f"{base_url}/d/{state['self_doctor']['portal_token']}/child/{state['children']['primary']['id']}/reminders/",
    )
    take_shot(session, asset_dir / "02-child-reminders.png")

    set_cookie_and_goto(
        session,
        cookie,
        f"{base_url}/d/{state['self_doctor']['portal_token']}/vaccine/{state['vaccines']['doctor_education_vaccine_id']}/",
    )
    take_shot(session, asset_dir / "03-doctor-vaccine-education.png")

    open_page(session, f"{base_url}/edu/patient/{state['vaccines']['patient_education_vaccine_id']}/?lang=en")
    take_shot(session, asset_dir / "04-patient-education-simple.png")


def capture_parent_flows(base_url: str, state: dict) -> None:
    slug = "parent-self-service-card-history-and-share-link"
    asset_dir = ensure_asset_dir(slug)
    session = SESSION
    clear_state(session, base_url)

    open_page(session, f"{base_url}/add/")
    take_shot(session, asset_dir / "01-parent-add-form.png")

    open_page(session, f"{base_url}/update/")
    take_shot(session, asset_dir / "02-parent-update-lookup.png")

    js(
        session,
        "\n".join(
            [
                f"await page.fill('#id_parent_whatsapp', {json.dumps(state['parents']['public']['whatsapp'])});",
                "await Promise.all([page.waitForLoadState('networkidle'), page.click('button[type=submit]')]);",
            ]
        ),
    )
    take_shot(session, asset_dir / "03-parent-select-child.png")

    js(session, f"await page.goto({json.dumps(base_url + '/card/' + str(state['children']['primary']['id']) + '/')});")
    time.sleep(0.5)
    take_shot(session, asset_dir / "04-parent-card.png")

    js(session, f"await page.goto({json.dumps(base_url + '/history/' + str(state['children']['secondary']['id']) + '/')});")
    time.sleep(0.5)
    take_shot(session, asset_dir / "05-parent-history.png")

    open_page(session, f"{base_url}/p/{state['children']['primary']['share_token']}/")
    take_shot(session, asset_dir / "06-share-link-verify.png")

    js(
        session,
        "\n".join(
            [
                f"await page.fill('#id_whatsapp', {json.dumps(state['parents']['public']['whatsapp'])});",
                "await Promise.all([page.waitForLoadState('networkidle'), page.click('button[type=submit]')]);",
            ]
        ),
    )
    take_shot(session, asset_dir / "07-share-link-card.png")

    js(
        session,
        f"await page.goto({json.dumps(base_url + '/edu/vaccine/' + str(state['vaccines']['patient_education_vaccine_id']) + '/?child=' + str(state['children']['primary']['id']))});",
    )
    time.sleep(0.5)
    take_shot(session, asset_dir / "08-parent-vaccine-education.png")


def main() -> None:
    if not PWCLI.exists():
        raise SystemExit(f"Playwright wrapper not found: {PWCLI}")
    if not STATE_PATH.exists():
        raise SystemExit(f"Demo state not found: {STATE_PATH}")

    state = load_state()
    base_url = os.environ.get("DOCS_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

    capture_overview(base_url)
    capture_admin_partner(base_url, state)
    capture_doctor_registration(base_url, state)
    capture_doctor_portal(base_url, state)
    capture_reminders_and_education(base_url, state)
    capture_parent_flows(base_url, state)

    print(f"Captured screenshots under {ASSET_ROOT}")


if __name__ == "__main__":
    main()
