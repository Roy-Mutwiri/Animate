from __future__ import annotations

import json
import mimetypes
import pickle
import sys
import re
import shutil
import threading
import traceback
import urllib.error
import urllib.request
import uuid
from dataclasses import asdict
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .pipeline import (
    EXTERNAL_UPLOADER,
    MANIFEST_DIR,
    DEFAULT_DELAY_MAX_SECONDS,
    DEFAULT_DELAY_MIN_SECONDS,
    DEFAULT_DAILY_POST_CAP,
    DEFAULT_STARTER_DELAY_MAX_SECONDS,
    DEFAULT_STARTER_DELAY_MIN_SECONDS,
    UploadBlockedError,
    analyze_youtube,
    clear_upload_block,
    existing_manifests_for_source,
    generate_from_youtube,
    load_posted_registry,
    read_manifest,
    run_uploader,
    upload_budget,
    upload_manifest,
    validate_upload_session,
)


if getattr(sys, "frozen", False):
    ROOT = Path(sys.executable).resolve().parent
else:
    ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "web"
ACCOUNT_META = ROOT / "data" / "account_meta.json"

JOBS: dict[str, dict[str, object]] = {}
JOBS_LOCK = threading.Lock()


def _safe_print(message: str) -> None:
    try:
        print(message)
    except OSError:
        pass


def _set_job(job_id: str, **values: object) -> None:
    with JOBS_LOCK:
        job = JOBS.setdefault(job_id, {})
        job.update(values)


def _append_log(job_id: str, message: str) -> None:
    with JOBS_LOCK:
        job = JOBS.setdefault(job_id, {})
        logs = job.setdefault("logs", [])
        assert isinstance(logs, list)
        logs.append(message)


def _set_progress(job_id: str, current: int, total: int, label: str) -> None:
    percent = 0 if total <= 0 else min(100, round((current / total) * 100))
    _set_job(
        job_id,
        progress={
            "current": current,
            "total": total,
            "percent": percent,
            "label": label,
        },
    )


def _user_error(value: object) -> dict[str, object]:
    text = str(value)
    lowered = text.lower()

    if "uploads for" in lowered and "paused" in lowered:
        return {
            "title": "Posting is paused for this TikTok account.",
            "cause": "The app paused posting because TikTok recently rejected this account before any video was posted.",
            "steps": [
                "Click Open TikTok for this account and log in again.",
                "After login succeeds, this pause is cleared automatically.",
                "Then try one small live upload before starting a large batch.",
            ],
        }
    if "daily posting budget" in lowered or "24-hour window" in lowered:
        return {
            "title": "Daily TikTok posting budget is used up.",
            "cause": text,
            "steps": [
                "Wait until older posts fall outside the 24-hour window.",
                "Use Preview only to continue checking clips without posting.",
                "Keep remaining ready clips queued for the next posting window.",
            ],
        }
    if "posting quota" in lowered or "rate-limited" in lowered or "rate limited" in lowered:
        return {
            "title": "TikTok is limiting this posting window.",
            "cause": text,
            "steps": [
                "Do not keep retrying live uploads from this account right now.",
                "Leave the remaining clips queued and wait for the cooldown to clear.",
                "Use Preview only if you want to keep checking the manifest without posting.",
            ],
        }
    if "status_code=8" in text or '"status_code": 8' in text or "project creation" in lowered:
        return {
            "title": "TikTok rejected this account before posting.",
            "cause": "TikTok did not accept the saved session for upload creation. No video was posted.",
            "steps": [
                "Click Open TikTok for this account and log in again.",
                "After login, try one small live upload before starting a large batch.",
                "If it fails again, wait several hours because TikTok may be rate-limiting this account.",
            ],
        }
    if "missing sessionid" in lowered or "missing tt-target-idc" in lowered or "no saved tiktok session" in lowered:
        return {
            "title": "TikTok login is missing or expired.",
            "cause": text,
            "steps": [
                "Click Open TikTok for this account.",
                "Log in until TikTok fully loads your account.",
                "Return here and start with Preview only, then try one live upload.",
            ],
        }
    if "upload stopped by user" in lowered or "stop requested" in lowered:
        return {
            "title": "Upload stopped.",
            "cause": "The job was stopped before it finished.",
            "steps": [
                "Start upload again when you are ready.",
                "Already uploaded clips will be skipped; ready clips remain queued.",
            ],
        }
    if "youtube" in lowered and ("unavailable" in lowered or "private" in lowered or "copyright" in lowered):
        return {
            "title": "YouTube video cannot be downloaded.",
            "cause": text,
            "steps": [
                "Open the YouTube link in your browser and confirm it plays.",
                "Use a public video or stream recording that is not private, age-restricted, or removed.",
                "Paste the corrected link and generate again.",
            ],
        }
    if "ffmpeg failed" in lowered:
        return {
            "title": "Clip rendering failed.",
            "cause": "The video renderer could not create this clip.",
            "steps": [
                "Check that the source video downloaded correctly.",
                "Try generating fewer clips or use a different section of the video.",
                "If the same clip keeps failing, regenerate the manifest.",
            ],
        }
    if "no face" in lowered or "chart section" in lowered:
        return {
            "title": "Clip validation failed.",
            "cause": text,
            "steps": [
                "Regenerate clips with a different layout or source video.",
                "Use Review to inspect failed clips before live upload.",
            ],
        }

    return {
        "title": "Something failed.",
        "cause": text or "The app could not finish this action.",
        "steps": [
            "Read the message above and fix that item first.",
            "Try the action again after the issue is corrected.",
            "If it repeats, send the Technical log to the developer.",
        ],
    }


def _fail_job(job_id: str, exc: Exception) -> None:
    user_message = _user_error(exc)
    _append_log(job_id, f"{user_message['title']} {user_message['cause']}")
    _safe_print(traceback.format_exc())
    _set_job(job_id, status="stopped" if _job_cancelled(job_id) else "failed", userMessage=user_message)


def _prune_complete_login_jobs() -> None:
    with JOBS_LOCK:
        stale = [
            job_id
            for job_id, job in JOBS.items()
            if job.get("status") == "complete" and job.get("title") == "TikTok login"
        ]
        for job_id in stale:
            JOBS.pop(job_id, None)


def _job_cancelled(job_id: str) -> bool:
    with JOBS_LOCK:
        return bool(JOBS.get(job_id, {}).get("cancel"))


def _cancel_running_jobs() -> int:
    count = 0
    with JOBS_LOCK:
        for job in JOBS.values():
            if job.get("status") in {"queued", "running"}:
                job["cancel"] = True
                job["status"] = "stopping"
                logs = job.setdefault("logs", [])
                if isinstance(logs, list):
                    logs.append("Stop requested by user.")
                count += 1
    return count


def _cancel_job(job_id: str) -> bool:
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job or job.get("status") not in {"queued", "running", "stopping"}:
            return False
        job["cancel"] = True
        job["status"] = "stopping"
        logs = job.setdefault("logs", [])
        if isinstance(logs, list):
            logs.append("Stop requested for this job.")
        return True


def _has_running_generate() -> bool:
    with JOBS_LOCK:
        return any(
            job.get("status") in {"queued", "running"} and job.get("title") == "Generating clips"
            for job in JOBS.values()
        )


def _has_running_upload() -> bool:
    with JOBS_LOCK:
        return any(
            job.get("status") in {"queued", "running", "stopping"} and job.get("title") == "Uploading clips"
            for job in JOBS.values()
        )


def _safe_manifest(path_value: str) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = ROOT / path
    path = path.resolve()
    root = ROOT.resolve()
    if root not in path.parents and path != root:
        raise ValueError("Manifest path is outside this project.")
    if path.suffix.lower() != ".csv":
        raise ValueError("Manifest must be a CSV file.")
    return path


def _account_status(account: str) -> dict[str, object]:
    cookie = EXTERNAL_UPLOADER / "CookiesDir" / f"tiktok_session-{account}.cookie"
    exists = cookie.exists() and cookie.stat().st_size > 2
    meta = _load_account_meta()
    display_name = str(meta.get(account, {}).get("displayName") or account)
    detected = bool(meta.get(account, {}).get("detected"))
    return {
        "account": account,
        "displayName": display_name,
        "detected": detected,
        "loggedIn": exists,
        "cookiePath": _relative(cookie),
        "message": "Saved session found" if exists else "No saved TikTok session for this label",
    }


def _account_limit_status(account: str) -> dict[str, object]:
    status = _account_status(account)
    budget = upload_budget(account)
    status["budget"] = budget
    status["limited"] = int(budget.get("remaining_24h", 0)) <= 0 and (
        int(budget.get("seconds_until_next", 0)) > 0 or int(budget.get("blocked_until", 0)) > 0
    )
    if budget.get("blocked_until"):
        status["limitReason"] = "TikTok cooldown"
    elif budget.get("remaining_24h", 0) <= 0 and budget.get("seconds_until_next", 0):
        status["limitReason"] = "24-hour automation budget"
    else:
        status["limitReason"] = ""
    return status


def _account_limits() -> list[dict[str, object]]:
    return [_account_limit_status(str(account["account"])) for account in _saved_accounts()]


def _clean_account_label(account: str) -> str:
    label = re.sub(r"[^A-Za-z0-9_-]", "", account.strip())
    if not label:
        raise ValueError("Account label must contain letters, numbers, underscores, or dashes.")
    return label[:40]


def _load_account_meta() -> dict[str, dict[str, str]]:
    if not ACCOUNT_META.exists():
        return {}
    try:
        value = json.loads(ACCOUNT_META.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _save_account_meta(meta: dict[str, dict[str, str]]) -> None:
    ACCOUNT_META.parent.mkdir(parents=True, exist_ok=True)
    ACCOUNT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def _set_account_display_name(account: str, display_name: str) -> None:
    meta = _load_account_meta()
    current = meta.setdefault(account, {})
    current["displayName"] = display_name.strip() or account
    current["detected"] = True
    _save_account_meta(meta)


def _ensure_account_label(account: str) -> dict[str, object]:
    label = _clean_account_label(account)
    meta = _load_account_meta()
    meta.setdefault(label, {})
    _save_account_meta(meta)
    return _account_status(label)


def _forget_account_label(account: str) -> bool:
    label = _clean_account_label(account)
    if label == "main":
        return False
    meta = _load_account_meta()
    removed = label in meta
    meta.pop(label, None)
    _save_account_meta(meta)
    return removed


def _cookie_header(account: str) -> str:
    cookie = EXTERNAL_UPLOADER / "CookiesDir" / f"tiktok_session-{account}.cookie"
    if not cookie.exists():
        return ""
    try:
        with cookie.open("rb") as f:
            values = pickle.load(f)
    except Exception:
        return ""
    if not isinstance(values, list):
        return ""
    parts = []
    for item in values:
        if isinstance(item, dict) and item.get("name") and item.get("value"):
            parts.append(f"{item['name']}={item['value']}")
    return "; ".join(parts)


def _find_username(value: object) -> str:
    if isinstance(value, dict):
        for key in ("uniqueId", "unique_id", "username", "userName"):
            found = value.get(key)
            if isinstance(found, str) and found.strip():
                return found.strip()
        for nested in value.values():
            found = _find_username(nested)
            if found:
                return found
    if isinstance(value, list):
        for nested in value:
            found = _find_username(nested)
            if found:
                return found
    return ""


def _detect_tiktok_username(account: str) -> str:
    cookies = _cookie_header(account)
    if not cookies:
        raise ValueError("No saved TikTok session cookie found for this account label.")

    urls = [
        "https://www.tiktok.com/passport/web/account/info/",
        "https://www.tiktok.com/api/user/detail/",
    ]
    headers = {
        "Cookie": cookies,
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        ),
        "Accept": "application/json,text/html,*/*",
        "Referer": "https://www.tiktok.com/",
    }

    errors: list[str] = []
    for url in urls:
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                body = response.read(900_000).decode("utf-8", errors="ignore")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            errors.append(str(exc))
            continue

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = None
        if parsed is not None:
            username = _find_username(parsed)
            if username:
                return username if username.startswith("@") else f"@{username}"

        for pattern in (
            r'"uniqueId"\s*:\s*"([^"]+)"',
            r'"unique_id"\s*:\s*"([^"]+)"',
            r'"username"\s*:\s*"([^"]+)"',
            r'"userName"\s*:\s*"([^"]+)"',
        ):
            match = re.search(pattern, body)
            if match and match.group(1).strip():
                username = match.group(1).strip()
                return username if username.startswith("@") else f"@{username}"

    detail = "; ".join(errors[-2:]) if errors else "TikTok did not return a username."
    raise RuntimeError(f"Could not detect TikTok username automatically. {detail}")


def _saved_accounts() -> list[dict[str, object]]:
    cookies_dir = EXTERNAL_UPLOADER / "CookiesDir"
    labels = set(_load_account_meta().keys())
    accounts: list[dict[str, object]] = []
    if cookies_dir.exists():
        for cookie in sorted(cookies_dir.glob("tiktok_session-*.cookie")):
            label = cookie.stem.replace("tiktok_session-", "", 1)
            labels.add(label)
    labels.add("main")
    for label in sorted(labels, key=lambda value: (value != "main", value.lower())):
        status = _account_status(label)
        cookie = EXTERNAL_UPLOADER / "CookiesDir" / f"tiktok_session-{label}.cookie"
        if cookie.exists():
            status["modified"] = cookie.stat().st_mtime
        accounts.append(status)
    return accounts


def _posted_history(account: str | None = None) -> list[dict[str, object]]:
    registry = load_posted_registry()
    posts: list[dict[str, object]] = []
    for key, item in registry.items():
        item_account = str(item.get("account", "unknown"))
        if account and item_account not in {account, "unknown"}:
            continue
        posts.append(
            {
                "key": key,
                "account": item_account,
                "clipPath": item.get("clip_path", ""),
                "caption": item.get("caption", ""),
                "sourceUrl": item.get("source_url", ""),
                "manifest": item.get("manifest", ""),
                "uploadedAt": item.get("uploaded_at", ""),
            }
        )
    posts.sort(key=lambda item: str(item.get("uploadedAt", "")), reverse=True)
    return posts


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _run_generate(job_id: str, payload: dict[str, object]) -> None:
    try:
        _set_job(job_id, status="running", title="Generating clips")
        _append_log(job_id, "Downloading YouTube source and preparing clips.")
        manifest = generate_from_youtube(
            youtube_url=str(payload["youtube"]),
            count=int(payload.get("count", 100)),
            min_seconds=int(payload.get("minSeconds", 30)),
            max_seconds=int(payload.get("maxSeconds", 50)),
            max_hashtags=int(payload.get("maxHashtags", 4)),
            seed=int(payload.get("seed", 42)),
            render_mode=str(payload.get("renderMode", "chart_face")),
            progress=lambda current, total, label: _set_progress(job_id, current, total, label),
            should_cancel=lambda: _job_cancelled(job_id),
        )
        _append_log(job_id, f"Manifest written: {_relative(manifest)}")
        _set_job(job_id, status="complete", manifest=_relative(manifest))
    except Exception as exc:
        _fail_job(job_id, exc)


def _run_login(job_id: str, payload: dict[str, object]) -> None:
    try:
        account = _clean_account_label(str(payload["account"]))
        _ensure_account_label(account)
        force_open = bool(payload.get("forceOpen", False))
        cookie = EXTERNAL_UPLOADER / "CookiesDir" / f"tiktok_session-{account}.cookie"
        backup: Path | None = None
        _set_job(job_id, status="running", title="TikTok login")
        _set_progress(job_id, 0, 1, "Opening TikTok login browser")
        _append_log(job_id, f"Opening TikTok login for account label: {account}")
        if force_open and cookie.exists():
            backup = cookie.with_suffix(f".cookie.backup-{datetime.now():%Y%m%d-%H%M%S}")
            shutil.copy2(cookie, backup)
            cookie.unlink()
            _append_log(job_id, f"Existing session backed up so TikTok can open again: {_relative(backup)}")
        result = run_uploader(["login", "-n", account])
        if _job_cancelled(job_id):
            _set_job(job_id, status="stopped")
            return
        if result.stdout:
            _append_log(job_id, result.stdout.strip())
        if result.returncode == 0:
            if clear_upload_block(account):
                _append_log(job_id, "Upload pause cleared automatically after successful login.")
            _set_progress(job_id, 1, 1, "Login complete")
            _set_job(job_id, status="complete")
            _prune_complete_login_jobs()
        else:
            if backup and backup.exists() and not cookie.exists():
                shutil.copy2(backup, cookie)
                _append_log(job_id, "Previous session restored because login did not complete.")
            raise RuntimeError(
                "TikTok login did not finish. Open TikTok again, scan the QR code or sign in, "
                "and wait until your TikTok home page loads before closing the browser."
            )
    except Exception as exc:
        _fail_job(job_id, exc)


def _run_upload(job_id: str, payload: dict[str, object]) -> None:
    try:
        _set_job(job_id, status="running", title="Uploading clips")
        manifest = _safe_manifest(str(payload["manifest"]))
        dry_run = bool(payload.get("dryRun", True))
        _append_log(job_id, f"Using manifest: {_relative(manifest)}")
        if dry_run:
            _append_log(job_id, "PREVIEW ONLY: dry run is on, so no TikTok posts will be made.")
        else:
            _append_log(job_id, "LIVE UPLOAD: dry run is off. Videos will be posted to TikTok.")
            _delay_min = int(payload.get("delayMinSeconds", DEFAULT_DELAY_MIN_SECONDS))
            _delay_max = int(payload.get("delayMaxSeconds", DEFAULT_DELAY_MAX_SECONDS))
            _append_log(
                job_id,
                (
                    f"Delay between posts: a random wait of "
                    f"{_delay_min // 60}-{_delay_max // 60} minutes. No post-count limit."
                ),
            )
        upload_manifest(
            manifest=manifest,
            account=_clean_account_label(str(payload["account"])),
            limit=None,
            delay_seconds=int(payload.get("delayMinSeconds", DEFAULT_DELAY_MIN_SECONDS)),
            dry_run=dry_run,
            progress=lambda current, total, label: _set_progress(job_id, current, total, label),
            delay_min_seconds=int(payload.get("delayMinSeconds", DEFAULT_DELAY_MIN_SECONDS)),
            delay_max_seconds=int(payload.get("delayMaxSeconds", DEFAULT_DELAY_MAX_SECONDS)),
            starter_count=int(payload.get("starterCount", 0)),
            starter_delay_min_seconds=int(payload.get("starterDelayMinSeconds", DEFAULT_STARTER_DELAY_MIN_SECONDS)),
            starter_delay_max_seconds=int(payload.get("starterDelayMaxSeconds", DEFAULT_STARTER_DELAY_MAX_SECONDS)),
            should_cancel=lambda: _job_cancelled(job_id),
        )
        _append_log(job_id, "Upload job finished.")
        _set_job(job_id, status="complete")
    except Exception as exc:
        _fail_job(job_id, exc)


class Handler(BaseHTTPRequestHandler):
    server_version = "TikTokPosterUI/1.0"

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        target = STATIC_DIR / "index.html" if parsed.path in ("", "/") else (STATIC_DIR / parsed.path.lstrip("/"))
        target = target.resolve()
        if STATIC_DIR.resolve() not in target.parents and target != STATIC_DIR.resolve():
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not target.exists() or not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(target.stat().st_size))
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/jobs":
            return self._json({"jobs": self._jobs()})
        if parsed.path == "/api/manifests":
            return self._json({"manifests": self._manifests()})
        if parsed.path == "/api/manifest":
            query = parse_qs(parsed.query)
            try:
                manifest = _safe_manifest(query.get("path", [""])[0])
                rows = [asdict(row) for row in read_manifest(manifest)]
                return self._json({"path": _relative(manifest), "rows": rows})
            except Exception as exc:
                return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        if parsed.path == "/api/analyze":
            query = parse_qs(parsed.query)
            url = query.get("youtube", [""])[0]
            min_seconds = int(query.get("minSeconds", ["30"])[0])
            max_seconds = int(query.get("maxSeconds", ["50"])[0])
            if not url:
                return self._json({"error": "YouTube URL is required."}, HTTPStatus.BAD_REQUEST)
            try:
                return self._json(analyze_youtube(url, min_seconds=min_seconds, max_seconds=max_seconds))
            except Exception as exc:
                return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        if parsed.path == "/api/account":
            query = parse_qs(parsed.query)
            account = query.get("account", ["main"])[0] or "main"
            return self._json(_account_status(account))
        if parsed.path == "/api/accounts":
            return self._json({"accounts": _saved_accounts()})
        if parsed.path == "/api/account-limits":
            return self._json({"accounts": _account_limits(), "dailyCap": DEFAULT_DAILY_POST_CAP})
        if parsed.path == "/api/posts":
            query = parse_qs(parsed.query)
            account = query.get("account", [""])[0] or None
            return self._json({"posts": _posted_history(account)})
        if parsed.path == "/api/upload-budget":
            query = parse_qs(parsed.query)
            account = query.get("account", ["main"])[0] or "main"
            try:
                return self._json(upload_budget(_clean_account_label(account)))
            except Exception as exc:
                return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

        return self._static(parsed.path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            payload = self._read_json()
        except Exception as exc:
            return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

        if parsed.path == "/api/generate":
            if not payload.get("youtube"):
                return self._json({"error": "YouTube URL is required."}, HTTPStatus.BAD_REQUEST)
            existing = existing_manifests_for_source(str(payload["youtube"]))
            if existing and not payload.get("forceRegenerate"):
                return self._json(
                    {
                        "error": "This YouTube link already has a generated manifest.",
                        "existingManifests": existing,
                    },
                    HTTPStatus.CONFLICT,
                )
            if _has_running_generate():
                return self._json(
                    {"error": "A clip generation job is already running. Wait for it to finish before starting another."},
                    HTTPStatus.CONFLICT,
                )
            job_id = self._start_job(_run_generate, payload)
            return self._json({"jobId": job_id}, HTTPStatus.ACCEPTED)

        if parsed.path == "/api/login":
            if not payload.get("account"):
                return self._json({"error": "Account label is required."}, HTTPStatus.BAD_REQUEST)
            job_id = self._start_job(_run_login, payload)
            return self._json({"jobId": job_id}, HTTPStatus.ACCEPTED)

        if parsed.path == "/api/account-name":
            account = str(payload.get("account") or "").strip()
            if not account:
                return self._json({"error": "Account label is required."}, HTTPStatus.BAD_REQUEST)
            try:
                display_name = _detect_tiktok_username(account)
            except Exception as exc:
                return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            _set_account_display_name(account, display_name)
            return self._json(_account_status(account))

        if parsed.path == "/api/account":
            account = str(payload.get("account") or "").strip()
            try:
                return self._json(_ensure_account_label(account))
            except Exception as exc:
                return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

        if parsed.path == "/api/account-forget":
            account = str(payload.get("account") or "").strip()
            try:
                removed = _forget_account_label(account)
            except Exception as exc:
                return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return self._json({"forgot": account, "removed": removed})

        if parsed.path == "/api/upload":
            if not payload.get("manifest") or not payload.get("account"):
                return self._json({"error": "Manifest and account are required."}, HTTPStatus.BAD_REQUEST)
            if _has_running_upload():
                return self._json(
                    {
                        "error": {
                            "title": "An upload is already running.",
                            "cause": "Starting another upload could post duplicate videos.",
                            "steps": [
                                "Wait for the current upload to finish, or click Stop on that job.",
                                "After it stops, refresh the manifest and start upload again.",
                                "Already uploaded clips will be skipped automatically.",
                            ],
                        }
                    },
                    HTTPStatus.CONFLICT,
                )
            if not bool(payload.get("dryRun", True)):
                account = _clean_account_label(str(payload["account"]))
                try:
                    validate_upload_session(account)
                except Exception as exc:
                    return self._json({"error": _user_error(exc)}, HTTPStatus.BAD_REQUEST)
            job_id = self._start_job(_run_upload, payload)
            return self._json({"jobId": job_id}, HTTPStatus.ACCEPTED)

        if parsed.path == "/api/stop":
            return self._json({"stopping": _cancel_running_jobs()})

        if parsed.path == "/api/stop-job":
            job_id = str(payload.get("jobId") or "").strip()
            if not job_id:
                return self._json({"error": "Job id is required."}, HTTPStatus.BAD_REQUEST)
            stopped = _cancel_job(job_id)
            if not stopped:
                return self._json({"error": "Job is not running or was not found."}, HTTPStatus.NOT_FOUND)
            return self._json({"stopping": job_id})

        return self._json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: object) -> None:
        _safe_print(f"[web] {self.address_string()} - {format % args}")

    def _start_job(self, target, payload: dict[str, object]) -> str:
        job_id = uuid.uuid4().hex[:10]
        _set_job(job_id, id=job_id, status="queued", logs=[])
        thread = threading.Thread(target=target, args=(job_id, payload), daemon=True)
        thread.start()
        return job_id

    def _jobs(self) -> list[dict[str, object]]:
        with JOBS_LOCK:
            return list(JOBS.values())[::-1]

    def _manifests(self) -> list[dict[str, object]]:
        if not MANIFEST_DIR.exists():
            return []
        items = []
        labels = ["Latest manifest", "Second newest", "Third newest"]
        paths = sorted(MANIFEST_DIR.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
        for position, path in enumerate(paths, start=1):
            rows = read_manifest(path)
            counts: dict[str, int] = {}
            for row in rows:
                counts[row.status] = counts.get(row.status, 0) + 1
            created = datetime.fromtimestamp(path.stat().st_mtime)
            label = labels[position - 1] if position <= len(labels) else f"Manifest {position}"
            display_name = f"{label} - {created:%b %d, %I:%M %p} - {len(rows)} clips"
            items.append(
                {
                    "path": _relative(path),
                    "name": path.name,
                    "displayName": display_name,
                    "order": position,
                    "count": len(rows),
                    "statuses": counts,
                    "modified": path.stat().st_mtime,
                }
            )
        return items

    def _read_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        if not raw:
            return {}
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError("JSON body must be an object.")
        return value

    def _json(self, data: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, request_path: str) -> None:
        if request_path in ("", "/"):
            request_path = "/index.html"
        target = (STATIC_DIR / request_path.lstrip("/")).resolve()
        if STATIC_DIR.resolve() not in target.parents and target != STATIC_DIR.resolve():
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not target.exists() or not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content = target.read_bytes()
        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run(host: str = "127.0.0.1", port: int = 8787) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    _safe_print(f"TikTok Poster UI running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _safe_print("Stopping server.")
    finally:
        server.server_close()
