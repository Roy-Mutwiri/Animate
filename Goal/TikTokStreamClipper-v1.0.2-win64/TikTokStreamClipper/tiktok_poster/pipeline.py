from __future__ import annotations

import csv
import json
import os
import pickle
import re
import random
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import asdict, dataclass, fields
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable

from yt_dlp import YoutubeDL

from .captions import make_caption


if getattr(sys, "frozen", False):
    ROOT = Path(sys.executable).resolve().parent
else:
    ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_UPLOADER = ROOT / "external" / "TiktokAutoUploader"
DATA_DIR = ROOT / "data"
SOURCE_DIR = DATA_DIR / "sources"
CLIPS_DIR = DATA_DIR / "clips"
MANIFEST_DIR = DATA_DIR / "manifests"
POSTED_REGISTRY = DATA_DIR / "posted_registry.json"
UPLOAD_BLOCKS = DATA_DIR / "upload_blocks.json"
FACE_CROP = (0.755, 0.51, 0.245, 0.43)
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("GLOG_minloglevel", "2")
_FACE_DETECTOR_LOCAL = threading.local()


@dataclass
class ClipRow:
    index: int
    source_url: str
    clip_path: str
    start_seconds: float
    duration_seconds: float
    caption: str
    status: str = "ready"
    uploaded_at: str = ""
    render_layout: str = ""


ProgressCallback = Callable[[int, int, str], None]
CancelCallback = Callable[[], bool]


class UploadBlockedError(RuntimeError):
    """Raised when TikTok rejects the account/session before any video can publish."""


HARD_UPLOAD_REJECTION_MARKERS = (
    "status_code=8",
    '"status_code": 8',
    "TikTok project create failed",
    "No cookie with Tiktok session id found",
    "No cookie with TikTok session id found",
)
UPLOAD_BLOCK_SECONDS = 6 * 60 * 60
QUOTA_BLOCK_SECONDS = 24 * 60 * 60
RATE_LIMIT_BLOCK_SECONDS = 2 * 60 * 60
# 0 means unlimited: there is no self-imposed cap on how many posts a run makes.
DEFAULT_DAILY_POST_CAP = 0
# Simple human-paced spacing: a random wait between 1 and 15 minutes per post,
# applied uniformly (no separate multi-hour "starter" phase).
DEFAULT_STARTER_DELAY_MIN_SECONDS = 1 * 60
DEFAULT_STARTER_DELAY_MAX_SECONDS = 15 * 60
DEFAULT_DELAY_MIN_SECONDS = 1 * 60
DEFAULT_DELAY_MAX_SECONDS = 15 * 60


QUOTA_REJECTION_MARKERS = (
    "spam_risk_too_many_posts",
    "reached_active_user_cap",
    "daily post cap",
    "daily quota",
)

RATE_LIMIT_REJECTION_MARKERS = (
    "rate_limit_exceeded",
    "too many requests",
    "status_code=429",
    '"status_code": 429',
    "HTTP 429",
)


def ensure_dirs() -> None:
    for path in (SOURCE_DIR, CLIPS_DIR, MANIFEST_DIR):
        path.mkdir(parents=True, exist_ok=True)


def source_key(url: str) -> str:
    patterns = (
        r"youtu\.be/([^?&/]+)",
        r"[?&]v=([^?&/]+)",
        r"youtube\.com/shorts/([^?&/]+)",
        r"youtube\.com/live/([^?&/]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, url or "")
        if match:
            return match.group(1)
    return (url or "").strip().lower()


def clip_key(row: ClipRow) -> str:
    start = round(float(row.start_seconds), 2)
    duration = round(float(row.duration_seconds), 2)
    return f"{source_key(row.source_url)}|{start}|{duration}"


def load_posted_registry() -> dict[str, dict[str, str]]:
    ensure_dirs()
    registry: dict[str, dict[str, str]] = {}
    if POSTED_REGISTRY.exists():
        try:
            with POSTED_REGISTRY.open("r", encoding="utf-8") as f:
                value = json.load(f)
                if isinstance(value, dict):
                    registry.update(value)
        except json.JSONDecodeError:
            registry = {}

    for manifest in MANIFEST_DIR.glob("*.csv"):
        try:
            rows = read_manifest(manifest)
        except Exception:
            continue
        for row in rows:
            if row.status == "uploaded":
                key = clip_key(row)
                entry = registry.setdefault(key, {})
                entry.setdefault("manifest", str(manifest))
                entry.setdefault("clip_path", row.clip_path)
                entry.setdefault("uploaded_at", row.uploaded_at or "unknown")
                entry.setdefault("caption", row.caption)
                entry.setdefault("source_url", row.source_url)
                entry.setdefault("account", "unknown")
    return registry


def save_posted_registry(registry: dict[str, dict[str, str]]) -> None:
    ensure_dirs()
    with POSTED_REGISTRY.open("w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def _parse_uploaded_at(value: object) -> float | None:
    if not value:
        return None
    text = str(value)
    try:
        return datetime.fromisoformat(text).timestamp()
    except ValueError:
        return None


UNLIMITED_REMAINING = 1_000_000_000


def upload_budget(account: str, daily_cap: int = DEFAULT_DAILY_POST_CAP) -> dict[str, int]:
    unlimited = daily_cap <= 0
    now = time.time()
    window_start = now - 24 * 60 * 60
    used = 0
    recent_times: list[float] = []
    for item in load_posted_registry().values():
        item_account = str(item.get("account", "unknown"))
        if item_account not in {account, "unknown"}:
            continue
        uploaded_at = _parse_uploaded_at(item.get("uploaded_at"))
        if uploaded_at is not None and uploaded_at >= window_start:
            used += 1
            recent_times.append(uploaded_at)
    if unlimited:
        remaining = UNLIMITED_REMAINING
    else:
        remaining = max(0, daily_cap - used)
    next_allowed_at = 0
    if not unlimited and remaining <= 0 and recent_times:
        recent_times.sort()
        cutoff_index = max(0, used - daily_cap)
        next_allowed_at = int(recent_times[cutoff_index] + 24 * 60 * 60)

    block = load_upload_blocks().get(account)
    blocked_until = 0
    if isinstance(block, dict):
        blocked_until = int(float(block.get("blocked_until") or 0))
        if blocked_until <= now:
            blocked_until = 0
    if blocked_until:
        remaining = 0
        next_allowed_at = max(next_allowed_at, blocked_until)

    seconds_until_next = max(0, int(next_allowed_at - now)) if next_allowed_at else 0
    return {
        "daily_cap": daily_cap,
        "used_24h": used,
        "remaining_24h": remaining,
        "next_allowed_at": next_allowed_at,
        "seconds_until_next": seconds_until_next,
        "blocked_until": blocked_until,
    }


def load_upload_blocks() -> dict[str, dict[str, object]]:
    if not UPLOAD_BLOCKS.exists():
        return {}
    try:
        value = json.loads(UPLOAD_BLOCKS.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def save_upload_blocks(blocks: dict[str, dict[str, object]]) -> None:
    ensure_dirs()
    UPLOAD_BLOCKS.write_text(json.dumps(blocks, indent=2), encoding="utf-8")


def block_account_uploads(account: str, reason: str) -> None:
    _block_account_uploads_for(account, reason, UPLOAD_BLOCK_SECONDS)


def block_account_quota(account: str, reason: str, seconds: int) -> None:
    _block_account_uploads_for(account, reason, seconds)


def _block_account_uploads_for(account: str, reason: str, seconds: int) -> None:
    blocks = load_upload_blocks()
    if _is_hard_upload_rejection(reason):
        reason = "TikTok rejected this account before posting. Please log in again, then try one small upload."
    elif _is_quota_rejection(reason):
        reason = "TikTok says this account or client has reached a posting quota. Wait for the posting window to clear."
    elif _is_rate_limit_rejection(reason):
        reason = "TikTok rate-limited upload creation. Wait before trying another live upload."
    blocks[account] = {
        "blocked_until": time.time() + seconds,
        "reason": reason,
        "blocked_at": datetime.now().isoformat(timespec="seconds"),
    }
    save_upload_blocks(blocks)


def clear_upload_block(account: str) -> bool:
    blocks = load_upload_blocks()
    removed = account in blocks
    blocks.pop(account, None)
    if removed:
        save_upload_blocks(blocks)
    return removed


def existing_manifests_for_source(url: str) -> list[str]:
    key = source_key(url)
    matches: list[str] = []
    for manifest in sorted(MANIFEST_DIR.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            rows = read_manifest(manifest)
        except Exception:
            continue
        if any(source_key(row.source_url) == key for row in rows):
            matches.append(str(manifest.relative_to(ROOT)))
    return matches


def ffmpeg_exe() -> str:
    path = shutil.which("ffmpeg")
    if path:
        return path
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise RuntimeError(
            "`ffmpeg` is required. Run `python -m pip install -r requirements.txt` "
            "or install FFmpeg and put it on PATH."
        ) from exc


def download_youtube(url: str, source_dir: Path, progress: ProgressCallback | None = None) -> tuple[Path, float]:
    ensure_dirs()
    source_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(source_dir / "%(id)s.%(ext)s")

    def download_hook(status: dict[str, object]) -> None:
        if not progress or status.get("status") != "downloading":
            return
        downloaded = int(status.get("downloaded_bytes") or 0)
        total = int(status.get("total_bytes") or status.get("total_bytes_estimate") or 0)
        if total > 0:
            progress(downloaded, total, "Downloading YouTube source")

    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": output_template,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "progress_hooks": [download_hook],
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        prepared = ydl.prepare_filename(info)
    path = Path(prepared).with_suffix(".mp4")
    if not path.exists():
        candidates = sorted(source_dir.glob(f"{info['id']}.*"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            raise RuntimeError("YouTube download finished, but no output file was found.")
        path = candidates[0]
    duration = info.get("duration")
    if not duration:
        raise RuntimeError("Could not determine source duration from YouTube metadata.")
    return path, float(duration)


def media_duration(video_path: Path) -> float:
    ffmpeg = ffmpeg_exe()
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(video_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stderr)
    if not match:
        raise RuntimeError(f"Could not read media duration for {video_path}.")
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def analyze_youtube(url: str, min_seconds: int = 30, max_seconds: int = 50) -> dict[str, object]:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "skip_download": True,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    duration = float(info.get("duration") or 0)
    if duration <= 0:
        raise RuntimeError("Could not determine video duration from YouTube metadata.")

    avg_seconds = (min_seconds + max_seconds) / 2
    min_count = max(1, int(duration // max_seconds))
    max_count = max(1, int(duration // min_seconds))
    recommended_count = max(1, int(duration // avg_seconds))

    return {
        "title": info.get("title") or "",
        "durationSeconds": duration,
        "durationLabel": _format_duration(duration),
        "minClipCount": min_count,
        "maxClipCount": max_count,
        "recommendedClipCount": recommended_count,
        "existingManifests": existing_manifests_for_source(url),
    }


def _format_duration(seconds: float) -> str:
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    return f"{minutes}m {secs}s"


def plan_clips(total_duration: float, count: int, min_seconds: int, max_seconds: int, seed: int) -> list[tuple[float, float]]:
    if count < 1:
        raise ValueError("count must be at least 1")
    if min_seconds < 1 or max_seconds < min_seconds:
        raise ValueError("seconds range is invalid")
    if total_duration < min_seconds:
        raise ValueError("source video is shorter than the requested minimum clip length")

    rng = random.Random(seed)
    usable = max(0.0, total_duration - max_seconds)
    starts: list[tuple[float, float]] = []
    for i in range(count):
        duration = rng.randint(min_seconds, max_seconds)
        base = 0 if count == 1 else usable * (i / count)
        spacing = usable / max(count, 1)
        jitter = rng.uniform(0, max(spacing - duration, 0)) if spacing > duration else 0
        start = min(base + jitter, max(0.0, total_duration - duration))
        starts.append((round(start, 2), float(duration)))
    return starts


def _mediapipe_face_boxes(frame) -> list[tuple[int, int, int, int]]:
    try:
        import cv2
        import mediapipe as mp
    except Exception:
        return []

    height, width = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    try:
        detector = getattr(_FACE_DETECTOR_LOCAL, "detector", None)
        if detector is None:
            detector = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.45)
            _FACE_DETECTOR_LOCAL.detector = detector
        result = detector.process(rgb)
    except Exception:
        return []
    boxes: list[tuple[int, int, int, int]] = []
    for detection in result.detections or []:
        box = detection.location_data.relative_bounding_box
        x = max(0, int(box.xmin * width))
        y = max(0, int(box.ymin * height))
        w = min(width - x, int(box.width * width))
        h = min(height - y, int(box.height * height))
        if w >= 35 and h >= 35:
            boxes.append((x, y, w, h))
    return boxes


def _opencv_face_boxes(frame, cascade) -> list[tuple[int, int, int, int]]:
    import cv2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=5, minSize=(55, 55))
    return [tuple(map(int, face)) for face in faces]


def _detect_face_crop(frame, cascade) -> tuple[bool, tuple[float, float, float, float]]:
    height, width = frame.shape[:2]
    faces = _mediapipe_face_boxes(frame) or _opencv_face_boxes(frame, cascade)
    if not faces:
        return False, FACE_CROP

    preferred = []
    for x, y, face_w, face_h in faces:
        center_x = x + face_w / 2
        center_y = y + face_h / 2
        if center_x >= width * 0.55 and center_y >= height * 0.35:
            preferred.append((x, y, face_w, face_h))
    candidates = preferred or faces
    x, y, face_w, face_h = max(candidates, key=lambda item: item[2] * item[3])

    center_x = x + face_w / 2
    center_y = y + face_h / 2
    crop_w = max(width * 0.245, face_w * 2.8)
    crop_h = max(height * 0.43, face_h * 3.2)
    crop_w = min(crop_w, width * 0.32)
    crop_h = min(crop_h, height * 0.58)
    crop_x = center_x - crop_w * 0.52
    crop_y = center_y - crop_h * 0.38

    crop_x = min(max(crop_x, 0), width - crop_w)
    crop_y = min(max(crop_y, 0), height - crop_h)
    return True, (crop_x / width, crop_y / height, crop_w / width, crop_h / height)


def _region_has_face(frame, cascade, region: tuple[float, float, float, float]) -> bool:
    height, width = frame.shape[:2]
    x_ratio, y_ratio, w_ratio, h_ratio = region
    x = int(width * x_ratio)
    y = int(height * y_ratio)
    region_w = int(width * w_ratio)
    region_h = int(height * h_ratio)
    crop = frame[y : y + region_h, x : x + region_w]
    if crop.size == 0:
        return False
    return bool(_mediapipe_face_boxes(crop) or _opencv_face_boxes(crop, cascade))


def _chart_region_visible(frame) -> bool:
    try:
        import cv2
    except Exception:
        return True

    height, width = frame.shape[:2]
    chart = frame[0 : int(height * 0.58), 0:width]
    if chart.size == 0:
        return False
    gray = cv2.cvtColor(chart, cv2.COLOR_BGR2GRAY)
    bright_ratio = float((gray > 35).mean())
    contrast = float(gray.std())
    return bright_ratio > 0.035 and contrast > 8.0


def face_crop_for_clip(video_path: Path, start: float, duration: float) -> tuple[bool, tuple[float, float, float, float]]:
    try:
        import cv2
    except Exception:
        return True, FACE_CROP

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if cascade.empty():
        return True, FACE_CROP

    start_offset = min(1.0, duration / 3)
    later_offsets = (min(5.0, duration / 2), duration / 2)
    cap = cv2.VideoCapture(str(video_path))
    try:
        first_crop: tuple[float, float, float, float] | None = None
        for offset in (start_offset, *later_offsets):
            cap.set(cv2.CAP_PROP_POS_MSEC, max(0.0, start + offset) * 1000)
            ok, frame = cap.read()
            if not ok or frame is None:
                continue
            visible, crop = _detect_face_crop(frame, cascade)
            if visible and offset == start_offset:
                first_crop = crop
            elif visible and first_crop is not None:
                return True, first_crop
        return False, FACE_CROP
    finally:
        cap.release()


def face_visible_in_webcam(video_path: Path, start: float, duration: float) -> bool:
    visible, _ = face_crop_for_clip(video_path, start, duration)
    return visible


def find_face_visible_start(
    source: Path,
    start: float,
    duration: float,
    total_duration: float,
    rng: random.Random,
    attempts: int = 80,
) -> tuple[float, tuple[float, float, float, float]]:
    visible, crop = face_crop_for_clip(source, start, duration)
    if visible:
        return start, crop

    usable = max(0.0, total_duration - duration)
    for _ in range(attempts):
        candidate = round(rng.uniform(0, usable), 2)
        visible, crop = face_crop_for_clip(source, candidate, duration)
        if visible:
            return candidate, crop
    return start, FACE_CROP


def validate_rendered_clip(clip_path: Path, layout: str) -> tuple[bool, str]:
    try:
        import cv2
    except Exception:
        return True, "OpenCV unavailable; skipped visual validation"

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if cascade.empty():
        return True, "OpenCV cascade unavailable; skipped visual validation"

    cap = cv2.VideoCapture(str(clip_path))
    try:
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 25)
        sample_frames = [max(0, int(fps * 0.8))]
        if frame_count > 4:
            sample_frames.append(max(0, frame_count // 2))

        saw_face = False
        saw_chart = layout != "chart_face"
        for frame_no in sample_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ok, frame = cap.read()
            if not ok or frame is None:
                continue
            if layout == "face_only":
                saw_face = saw_face or _region_has_face(frame, cascade, (0.0, 0.0, 1.0, 1.0))
            elif layout == "chart_face":
                saw_face = saw_face or _region_has_face(frame, cascade, (0.0, 0.55, 1.0, 0.45))
                saw_chart = saw_chart or _chart_region_visible(frame)

        if layout == "face_only" and not saw_face:
            return False, "Face-only validation failed: no face detected in rendered clip"
        if layout == "chart_face":
            if not saw_face:
                return False, "Face + charts validation failed: no face detected in bottom section"
            if not saw_chart:
                return False, "Face + charts validation failed: chart section was not visible"
        return True, "Validated"
    finally:
        cap.release()


def render_filter(layout: str, duration: float, face_crop: tuple[float, float, float, float] | None = None) -> str:
    face_x, face_y, face_w, face_h = face_crop or FACE_CROP
    if layout == "face_only":
        return (
            f"[0:v]crop=w=iw*{face_w}:h=ih*{face_h}:x=iw*{face_x}:y=ih*{face_y},"
            "setpts=PTS-STARTPTS,"
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,setsar=1,format=yuv420p[v]"
        )
    if layout == "chart_face":
        return (
            "[0:v]crop=w=iw*0.74:h=ih*0.82:x=0:y=ih*0.06,"
            "setpts=PTS-STARTPTS,"
            "scale=1080:1180:force_original_aspect_ratio=increase,"
            "crop=1080:1180,setsar=1[chart];"
            f"[0:v]crop=w=iw*{face_w}:h=ih*{face_h}:x=iw*{face_x}:y=ih*{face_y},"
            "setpts=PTS-STARTPTS,"
            "scale=1080:740:force_original_aspect_ratio=increase,"
            "crop=1080:740,setsar=1[face];"
            f"color=c=black:s=1080x1920:d={duration}[base];"
            "[base][chart]overlay=0:0[tmp];"
            "[tmp][face]overlay=0:1180,format=yuv420p[v]"
        )
    return (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,format=yuv420p[v]"
    )


def choose_render_layout(index: int, render_mode: str) -> str:
    if render_mode in {"face_only", "chart_face"}:
        return render_mode
    return "chart_face"


def render_clip(
    source: Path,
    output: Path,
    start: float,
    duration: float,
    layout: str = "chart_face",
    face_crop: tuple[float, float, float, float] | None = None,
) -> None:
    ffmpeg = ffmpeg_exe()
    output.parent.mkdir(parents=True, exist_ok=True)
    vf = render_filter(layout, duration, face_crop=face_crop)
    def build_cmd(include_audio: bool) -> list[str]:
        cmd = [
            ffmpeg,
            "-y",
            "-ss",
            str(start),
            "-t",
            str(duration),
            "-i",
            str(source),
            "-filter_complex",
            vf,
            "-map",
            "[v]",
        ]
        if include_audio:
            cmd.extend(["-map", "0:a?", "-c:a", "aac", "-b:a", "128k"])
        cmd.extend(
            [
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "23",
                "-movflags",
                "+faststart",
                str(output),
            ]
        )
        return cmd

    first = subprocess.run(build_cmd(include_audio=True), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if first.returncode == 0:
        return

    if output.exists():
        output.unlink()
    second = subprocess.run(build_cmd(include_audio=False), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if second.returncode != 0:
        tail = "\n".join((second.stderr or second.stdout or first.stderr or first.stdout).splitlines()[-25:])
        raise RuntimeError(f"FFmpeg failed for {output.name} at {start}s for {duration}s:\n{tail}")


def write_manifest(rows: Iterable[ClipRow], path: Path) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [field.name for field in fields(ClipRow)]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def read_manifest(path: Path) -> list[ClipRow]:
    defaults = {field.name: field.default for field in fields(ClipRow)}
    required_defaults = {
        "index": 0,
        "source_url": "",
        "clip_path": "",
        "start_seconds": 0.0,
        "duration_seconds": 0.0,
        "caption": "",
    }
    defaults.update(required_defaults)
    rows: list[ClipRow] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            cleaned = {field.name: raw.get(field.name, defaults[field.name]) for field in fields(ClipRow)}
            try:
                cleaned["index"] = int(cleaned["index"] or 0)
            except (TypeError, ValueError):
                cleaned["index"] = 0
            for name in ("start_seconds", "duration_seconds"):
                try:
                    cleaned[name] = float(cleaned[name] or 0)
                except (TypeError, ValueError):
                    cleaned[name] = 0.0
            rows.append(ClipRow(**cleaned))
    return rows


def update_manifest(path: Path, rows: list[ClipRow]) -> None:
    write_manifest(rows, path)


def generate_from_youtube(
    youtube_url: str,
    count: int,
    min_seconds: int = 30,
    max_seconds: int = 50,
    seed: int = 42,
    max_hashtags: int = 4,
    render_mode: str = "chart_face",
    progress: ProgressCallback | None = None,
    should_cancel: CancelCallback | None = None,
) -> Path:
    ensure_dirs()
    batch = datetime.now().strftime("%Y%m%d-%H%M%S")
    batch_dir = CLIPS_DIR / batch
    source_dir = SOURCE_DIR / batch
    manifest = MANIFEST_DIR / f"{batch}.csv"

    if progress:
        progress(0, count, "Downloading YouTube source")
    source, metadata_duration = download_youtube(youtube_url, source_dir=source_dir, progress=progress)
    file_duration = media_duration(source)
    duration = min(metadata_duration, file_duration)
    if progress:
        progress(0, count, f"Planning clips from {int(duration)} seconds of downloaded video")
    planned = plan_clips(duration, count, min_seconds, max_seconds, seed)
    rng = random.Random(seed)
    rows: list[ClipRow] = []

    for index, (start, length) in enumerate(planned, start=1):
        if should_cancel and should_cancel():
            raise RuntimeError("Generation stopped by user")
        layout = choose_render_layout(index, render_mode)
        face_crop = FACE_CROP
        output = batch_dir / f"clip-{index:04d}.mp4"
        validation_note = ""
        for render_attempt in range(1, 7):
            if should_cancel and should_cancel():
                raise RuntimeError("Generation stopped by user")
            if layout in {"face_only", "chart_face"}:
                if progress:
                    progress(
                        index - 1,
                        count,
                        f"Checking face visibility for clip {index} of {count} (attempt {render_attempt})",
                    )
                candidate_start = start if render_attempt == 1 else rng.uniform(0, max(0.0, duration - length))
                visible_start, face_crop = find_face_visible_start(source, candidate_start, length, duration, rng)
                if visible_start != start:
                    start = visible_start
                    if progress:
                        progress(index - 1, count, f"Moved clip {index} to a visible-face timestamp")
            if progress:
                progress(index - 1, count, f"Rendering clip {index} of {count} ({layout})")
            render_clip(source, output, start, length, layout=layout, face_crop=face_crop)
            valid, validation_note = validate_rendered_clip(output, layout)
            if valid:
                break
            if output.exists():
                output.unlink()
            if progress:
                progress(index - 1, count, f"{validation_note}; retrying clip {index}")
        else:
            raise RuntimeError(f"Could not render a valid {layout} clip for item {index}: {validation_note}")
        rows.append(
            ClipRow(
                index=index,
                source_url=youtube_url,
                clip_path=str(output),
                start_seconds=start,
                duration_seconds=length,
                caption=make_caption(index, rng, max_hashtags=max_hashtags),
                render_layout=layout,
            )
        )
        write_manifest(rows, manifest)
        if progress:
            progress(index, count, f"Rendered clip {index} of {count}")

    write_manifest(rows, manifest)
    return manifest


def _uploader_python() -> str:
    """Return a real Python interpreter for running the external uploader.

    When running as a normal script, ``sys.executable`` is the Python
    interpreter and can be used directly. When running from the frozen .exe,
    ``sys.executable`` is the app itself (not Python), so we must locate a
    system Python on PATH to run the uploader's ``cli.py``.
    """
    if not getattr(sys, "frozen", False):
        return sys.executable

    for candidate in ("python", "python3", "py"):
        found = shutil.which(candidate)
        if found:
            return found

    raise RuntimeError(
        "Python is required to log in and upload to TikTok, but it was not "
        "found on your PATH. Install Python 3.11+ from https://www.python.org/downloads/ "
        "(tick 'Add python.exe to PATH'), then install the uploader dependencies:\n"
        "  python -m pip install -r external\\TiktokAutoUploader\\requirements.txt\n"
        "See HOW-TO-USE.md for the one-time upload setup."
    )


def run_uploader(args: list[str]) -> subprocess.CompletedProcess[str]:
    if not EXTERNAL_UPLOADER.exists():
        raise RuntimeError(f"Missing uploader repo at {EXTERNAL_UPLOADER}")
    env = os.environ.copy()
    env.setdefault("TIKTOK_LOGIN_URL", "https://www.tiktok.com/login")
    return subprocess.run(
        [_uploader_python(), "cli.py", *args],
        cwd=EXTERNAL_UPLOADER,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def login(account: str) -> int:
    result = run_uploader(["login", "-n", account])
    print(result.stdout)
    return result.returncode


def validate_upload_session(account: str) -> None:
    block = load_upload_blocks().get(account)
    if isinstance(block, dict):
        blocked_until = float(block.get("blocked_until") or 0)
        if blocked_until > time.time():
            minutes = max(1, round((blocked_until - time.time()) / 60))
            reason = str(
                block.get("reason")
                or "TikTok recently rejected this account before posting. Please log in again, then try one small upload."
            )
            if _is_hard_upload_rejection(reason):
                reason = "TikTok rejected this account before posting. Please log in again, then try one small upload."
                block["reason"] = reason
                save_upload_blocks(load_upload_blocks() | {account: block})
            elif _is_quota_rejection(reason):
                reason = "TikTok says this account or client has reached a posting quota. Wait for the posting window to clear."
                block["reason"] = reason
                save_upload_blocks(load_upload_blocks() | {account: block})
            elif _is_rate_limit_rejection(reason):
                reason = "TikTok rate-limited upload creation. Wait before trying another live upload."
                block["reason"] = reason
                save_upload_blocks(load_upload_blocks() | {account: block})
            raise UploadBlockedError(
                f"Uploads for '{account}' are paused for about {minutes} more minute(s). {reason}"
            )
    cookie = EXTERNAL_UPLOADER / "CookiesDir" / f"tiktok_session-{account}.cookie"
    if not cookie.exists() or cookie.stat().st_size <= 2:
        raise UploadBlockedError(f"No saved TikTok session for account '{account}'. Open TikTok and log in first.")
    try:
        with cookie.open("rb") as f:
            cookies = pickle.load(f)
    except Exception as exc:
        raise UploadBlockedError(f"Saved TikTok session for '{account}' is unreadable. Re-login this account.") from exc
    if not isinstance(cookies, list):
        raise UploadBlockedError(f"Saved TikTok session for '{account}' has an invalid format. Re-login this account.")
    names = {item.get("name") for item in cookies if isinstance(item, dict)}
    missing = [name for name in ("sessionid", "tt-target-idc") if name not in names]
    if missing:
        raise UploadBlockedError(
            f"Saved TikTok session for '{account}' is missing {', '.join(missing)}. Re-login this account."
        )


def _output_tail(output: str, max_lines: int = 8) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return " | ".join(lines[-max_lines:])


def _is_hard_upload_rejection(output: str) -> bool:
    return any(marker in output for marker in HARD_UPLOAD_REJECTION_MARKERS)


def _is_quota_rejection(output: str) -> bool:
    lowered = output.lower()
    return any(marker in lowered for marker in QUOTA_REJECTION_MARKERS)


def _is_rate_limit_rejection(output: str) -> bool:
    lowered = output.lower()
    return any(marker.lower() in lowered for marker in RATE_LIMIT_REJECTION_MARKERS)


def upload_manifest(
    manifest: Path,
    account: str,
    limit: int | None,
    delay_seconds: int,
    dry_run: bool,
    progress: ProgressCallback | None = None,
    delay_min_seconds: int | None = None,
    delay_max_seconds: int | None = None,
    starter_count: int = 0,
    starter_delay_min_seconds: int = DEFAULT_STARTER_DELAY_MIN_SECONDS,
    starter_delay_max_seconds: int = DEFAULT_STARTER_DELAY_MAX_SECONDS,
    daily_post_cap: int = DEFAULT_DAILY_POST_CAP,
    should_cancel: CancelCallback | None = None,
) -> None:
    rows = read_manifest(manifest)
    registry = load_posted_registry()
    changed = False
    for row in rows:
        if row.status == "ready" and clip_key(row) in registry:
            row.status = "uploaded"
            row.uploaded_at = registry[clip_key(row)].get("uploaded_at", "previously-posted")
            changed = True
    if changed:
        update_manifest(manifest, rows)

    ready_indexes = [i for i, row in enumerate(rows) if row.status == "ready"]
    if limit is not None:
        ready_indexes = ready_indexes[:limit]
    if ready_indexes and not dry_run:
        # Only enforce a self-imposed daily cap when one is explicitly set
        # (daily_post_cap > 0). With the default of 0 there is no cap.
        if daily_post_cap > 0:
            budget = upload_budget(account, daily_cap=daily_post_cap)
            if budget["remaining_24h"] <= 0:
                wait = _format_wait_seconds(int(budget.get("seconds_until_next") or 0))
                raise UploadBlockedError(
                    f"Daily posting budget for '{account}' is used up: "
                    f"{budget['used_24h']}/{budget['daily_cap']} posts in the last 24 hours. "
                    f"Wait about {wait} before posting more."
                )
            if len(ready_indexes) > budget["remaining_24h"]:
                ready_indexes = ready_indexes[: budget["remaining_24h"]]
                if progress:
                    progress(
                        0,
                        len(ready_indexes),
                        (
                            f"Limited this live run to {budget['remaining_24h']} post(s), "
                            f"because {budget['used_24h']}/{budget['daily_cap']} were posted in the last 24 hours"
                        ),
                    )
        # Still stop early if TikTok itself has rejected/blocked this account.
        validate_upload_session(account)

    if delay_min_seconds is None:
        delay_min_seconds = delay_seconds or DEFAULT_DELAY_MIN_SECONDS
    if delay_max_seconds is None:
        delay_max_seconds = delay_seconds or DEFAULT_DELAY_MAX_SECONDS
    if delay_min_seconds < 0 or delay_max_seconds < 0 or delay_min_seconds > delay_max_seconds:
        raise ValueError("Delay range is invalid")
    if starter_count < 0:
        raise ValueError("Starter count cannot be negative")
    if daily_post_cap < 0:
        raise ValueError("Daily post cap cannot be negative (use 0 for unlimited)")
    if (
        starter_delay_min_seconds < 0
        or starter_delay_max_seconds < 0
        or starter_delay_min_seconds > starter_delay_max_seconds
    ):
        raise ValueError("Starter delay range is invalid")
    rng = random.Random()
    uploaded_count = 0
    failed_count = 0
    rejected_upload_count = 0

    for pos, row_index in enumerate(ready_indexes, start=1):
        if should_cancel and should_cancel():
            raise RuntimeError("Upload stopped by user")
        row = rows[row_index]
        if progress:
            progress(pos - 1, len(ready_indexes), f"Preparing {Path(row.clip_path).name}")
        print(f"[{pos}/{len(ready_indexes)}] {Path(row.clip_path).name}: {row.caption}")
        if dry_run:
            if progress:
                progress(pos, len(ready_indexes), f"Dry-run checked {Path(row.clip_path).name}")
            continue
        layout = row.render_layout or "chart_face"
        clip_path = Path(row.clip_path)
        if not clip_path.exists():
            row.status = "failed"
            failed_count += 1
            update_manifest(manifest, rows)
            if progress:
                progress(pos, len(ready_indexes), f"Skipped missing file {clip_path.name}")
            continue
        valid, validation_note = validate_rendered_clip(clip_path, layout)
        if not valid:
            row.status = "failed"
            failed_count += 1
            update_manifest(manifest, rows)
            if progress:
                progress(pos, len(ready_indexes), f"Skipped invalid {clip_path.name}: {validation_note}")
            continue
        result = run_uploader(["upload", "-u", account, "-v", str(clip_path), "-t", row.caption])
        print(result.stdout)
        if result.returncode == 0 and "Published successfully" in result.stdout:
            row.status = "uploaded"
            row.uploaded_at = datetime.now().isoformat(timespec="seconds")
            registry[clip_key(row)] = {
                "manifest": str(manifest),
                "clip_path": row.clip_path,
                "uploaded_at": row.uploaded_at,
                "account": account,
                "caption": row.caption,
                "source_url": row.source_url,
            }
            save_posted_registry(registry)
            update_manifest(manifest, rows)
            clear_upload_block(account)
            uploaded_count += 1
            if progress:
                progress(pos, len(ready_indexes), f"Uploaded {Path(row.clip_path).name}")
        else:
            rejected_upload_count += 1
            detail = _output_tail(result.stdout) or f"exit code {result.returncode}"
            if _is_hard_upload_rejection(result.stdout):
                row.status = "failed"
                failed_count += 1
                update_manifest(manifest, rows)
                user_label = (
                    f"TikTok rejected login/session for {Path(row.clip_path).name}. "
                    "Open TikTok and log in again before retrying."
                )
                if progress:
                    progress(pos, len(ready_indexes), user_label)
                block_account_uploads(account, detail)
                raise UploadBlockedError(
                    "TikTok rejected project creation before publishing. "
                    f"Stopped after {rejected_upload_count} rejected upload attempt(s); "
                    "remaining clips were left ready. Re-login the account or wait for the TikTok limit to clear."
                )
            if _is_quota_rejection(result.stdout):
                block_account_quota(account, detail, QUOTA_BLOCK_SECONDS)
                if progress:
                    progress(
                        pos,
                        len(ready_indexes),
                        "TikTok reported a posting quota. Stopped now and left the queue ready for tomorrow.",
                    )
                raise UploadBlockedError(
                    "TikTok reported that this account or client reached a posting quota. "
                    "Stopped immediately and left this clip plus remaining ready clips queued."
                )
            if _is_rate_limit_rejection(result.stdout):
                block_account_quota(account, detail, RATE_LIMIT_BLOCK_SECONDS)
                if progress:
                    progress(
                        pos,
                        len(ready_indexes),
                        "TikTok rate-limited upload creation. Stopped now and left the queue ready.",
                    )
                raise UploadBlockedError(
                    "TikTok rate-limited upload creation. Stopped immediately and left this clip plus remaining ready clips queued."
                )
            row.status = "failed"
            failed_count += 1
            update_manifest(manifest, rows)
            if progress:
                progress(pos, len(ready_indexes), f"Upload failed for {Path(row.clip_path).name}: {detail}")
            continue

        if pos <= starter_count:
            wait_min = starter_delay_min_seconds
            wait_max = starter_delay_max_seconds
            wait_label = "starter"
        else:
            wait_min = delay_min_seconds
            wait_max = delay_max_seconds
            wait_label = "normal"

        wait_seconds = rng.randint(wait_min, wait_max) if wait_max else 0
        if wait_seconds and pos < len(ready_indexes):
            for remaining in range(wait_seconds, 0, -1):
                if should_cancel and should_cancel():
                    raise RuntimeError("Upload stopped by user")
                if progress:
                    minutes, seconds = divmod(remaining, 60)
                    progress(
                        pos,
                        len(ready_indexes),
                        f"Waiting {minutes:02d}:{seconds:02d} before next upload ({wait_label} delay)",
                    )
                time.sleep(1)

    if ready_indexes and not dry_run and uploaded_count == 0 and rejected_upload_count > 0:
        raise UploadBlockedError(f"No clips uploaded. TikTok rejected {rejected_upload_count} upload attempt(s).")


def manifest_summary(path: Path) -> dict[str, int]:
    rows = read_manifest(path)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    counts["total"] = len(rows)
    return counts


def _format_wait_seconds(total_seconds: int) -> str:
    seconds = max(0, int(total_seconds))
    if seconds <= 0:
        return "0 minutes"
    hours, remainder = divmod(seconds, 3600)
    minutes = max(1, round(remainder / 60)) if remainder else 0
    if hours and minutes:
        return f"{hours} hour(s) {minutes} minute(s)"
    if hours:
        return f"{hours} hour(s)"
    return f"{minutes} minute(s)"
