import csv
import json
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\Animate\Goal")
STUDY = Path(r"D:\Animate\Projects\HonestInterview\ReferenceStudy")
SHEETS = STUDY / "contact_sheets"
FRAMES = STUDY / "frames"
REPORTS = STUDY / "reports"


def safe_name(name: str) -> str:
    keep = []
    for ch in name:
        keep.append(ch if ch.isalnum() or ch in "._- " else "_")
    return "".join(keep).strip().replace(" ", "_")


def ffprobe(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-show_entries", "stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames,duration",
        "-of", "json", str(path),
    ]
    return json.loads(subprocess.check_output(cmd, text=True, encoding="utf-8"))


def rate_to_float(rate: str) -> float:
    if not rate or rate == "0/0":
        return 0.0
    a, b = rate.split("/")
    return float(a) / float(b)


def label_image(img, label, width=320):
    h, w = img.shape[:2]
    scale = width / w
    nh = int(h * scale)
    resized = cv2.resize(img, (width, nh), interpolation=cv2.INTER_AREA)
    pil = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    band = 36
    out = Image.new("RGB", (width, nh + band), (245, 239, 226))
    out.paste(pil, (0, band))
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, width, band], fill=(32, 24, 20))
    d.text((8, 9), label, fill=(255, 247, 230))
    return out


def make_sheet(images, cols, out_path):
    if not images:
        return
    w, h = images[0].size
    rows = math.ceil(len(images) / cols)
    sheet = Image.new("RGB", (cols * w, rows * h), (250, 242, 226))
    for i, im in enumerate(images):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(out_path, quality=95)


def sample_packet_durations(path: Path) -> list[float]:
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=duration_time", "-of", "csv=p=0", str(path)]
    vals = []
    for line in subprocess.check_output(cmd, text=True, encoding="utf-8", errors="replace").splitlines():
        try:
            if line.strip():
                vals.append(round(float(line.strip()), 6))
        except ValueError:
            pass
    return vals


def create_inventory():
    rows = []
    for path in sorted(ROOT.glob("*.mp4")):
        data = ffprobe(path)
        streams = data.get("streams", [])
        video = next((s for s in streams if s.get("codec_type") == "video"), {})
        audio = [s for s in streams if s.get("codec_type") == "audio"]
        packets = sample_packet_durations(path)
        unique_packets = sorted(set(packets))
        rows.append({
            "filename": path.name,
            "path": str(path),
            "bytes": path.stat().st_size,
            "duration": data.get("format", {}).get("duration", ""),
            "width": video.get("width", ""),
            "height": video.get("height", ""),
            "r_frame_rate": video.get("r_frame_rate", ""),
            "avg_frame_rate": video.get("avg_frame_rate", ""),
            "nb_frames": video.get("nb_frames", ""),
            "video_codec": video.get("codec_name", ""),
            "audio": ";".join(f"{s.get('codec_name')} dur={s.get('duration', '')}" for s in audio) or "none",
            "packet_duration_values": "|".join(map(str, unique_packets[:12])),
            "variable_frame_timing": len(unique_packets) > 1,
        })
    with (REPORTS / "reference_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def frame_at(cap, frame_index):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ok, frame = cap.read()
    return frame if ok else None


def create_overview_and_shots(path: Path):
    data = ffprobe(path)
    video = next(s for s in data["streams"] if s.get("codec_type") == "video")
    fps = rate_to_float(video["avg_frame_rate"])
    frames = int(video.get("nb_frames") or 0)
    duration = float(data["format"]["duration"])
    stem = safe_name(path.stem)
    cap = cv2.VideoCapture(str(path))

    # One frame per second overview.
    overview_imgs = []
    for sec in range(int(math.floor(duration)) + 1):
        idx = min(frames - 1, int(round(sec * fps)))
        fr = frame_at(cap, idx)
        if fr is not None:
            overview_imgs.append(label_image(fr, f"{path.name} | t={sec:05.2f}s f={idx}", width=240))
    make_sheet(overview_imgs, 4, SHEETS / f"{stem}__overview_1s.jpg")

    # Detect shot/action boundaries with histogram deltas plus sparse frame hold spans.
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    prev_hist = None
    prev_gray = None
    rows = []
    shot_breaks = [0]
    hold_start = 0
    last_sig = None
    for i in range(frames):
        ok, fr = cap.read()
        if not ok:
            break
        small = cv2.resize(fr, (160, 90), interpolation=cv2.INTER_AREA)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [24, 24], [0, 180, 0, 256])
        cv2.normalize(hist, hist)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        diff = 0.0 if prev_gray is None else float(np.mean(cv2.absdiff(gray, prev_gray)))
        hdiff = 0.0 if prev_hist is None else float(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA))
        if i and (hdiff > 0.42 or diff > 42):
            shot_breaks.append(i)
        sig = cv2.resize(gray, (32, 18), interpolation=cv2.INTER_AREA)
        sig = (sig // 8).astype(np.uint8).tobytes()
        if last_sig is not None and sig != last_sig:
            if i - hold_start > max(2, int(fps * 0.20)):
                rows.append({"type": "holdish_span", "start_frame": hold_start, "end_frame": i - 1, "start_time": hold_start / fps, "end_time": (i - 1) / fps})
            hold_start = i
        last_sig = sig
        prev_hist = hist
        prev_gray = gray
    shot_breaks.append(frames)
    for a, b in zip(shot_breaks, shot_breaks[1:]):
        rows.append({"type": "shot_or_cut", "start_frame": a, "end_frame": b - 1, "start_time": a / fps, "end_time": (b - 1) / fps})
    with (REPORTS / f"{stem}__detected_segments.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["type", "start_frame", "end_frame", "start_time", "end_time"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    cap.release()
    return fps, frames, duration


def create_consecutive_contact_sheets(path: Path, start_frame=0, end_frame=None, step=1, frames_per_sheet=24, thumb_width=220):
    data = ffprobe(path)
    video = next(s for s in data["streams"] if s.get("codec_type") == "video")
    fps = rate_to_float(video["avg_frame_rate"])
    total = int(video.get("nb_frames") or 0)
    end_frame = total - 1 if end_frame is None else min(end_frame, total - 1)
    stem = safe_name(path.stem)
    out_dir = SHEETS / f"{stem}__frames_{start_frame:05d}_{end_frame:05d}_step{step}"
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(path))
    images = []
    sheet_no = 1
    manifest_rows = []
    for idx in range(start_frame, end_frame + 1, step):
        fr = frame_at(cap, idx)
        if fr is None:
            continue
        images.append(label_image(fr, f"{idx} | {idx/fps:0.3f}s", width=thumb_width))
        if len(images) == frames_per_sheet:
            out = out_dir / f"sheet_{sheet_no:04d}_f{idx-(frames_per_sheet-1)*step:05d}-{idx:05d}.jpg"
            make_sheet(images, 4, out)
            manifest_rows.append((out.name, idx - (frames_per_sheet - 1) * step, idx))
            images = []
            sheet_no += 1
    if images:
        last = end_frame
        first = last - (len(images) - 1) * step
        out = out_dir / f"sheet_{sheet_no:04d}_f{first:05d}-{last:05d}.jpg"
        make_sheet(images, 4, out)
        manifest_rows.append((out.name, first, last))
    cap.release()
    with (out_dir / "sheet_index.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sheet", "start_frame", "end_frame", "start_time", "end_time", "visual_inspection_status"])
        for name, a, b in manifest_rows:
            w.writerow([name, a, b, a / fps, b / fps, "not_yet_inspected"])
    return out_dir


if __name__ == "__main__":
    for d in (SHEETS, FRAMES, REPORTS):
        d.mkdir(parents=True, exist_ok=True)
    rows = create_inventory()
    for row in rows:
        path = Path(row["path"])
        fps, frames, duration = create_overview_and_shots(path)
        # Full consecutive sheets for all short references and the primary first 8 seconds.
        if path.name == "Bro was so honest.mp4":
            create_consecutive_contact_sheets(path, 0, min(frames - 1, int(round(8 * fps)) - 1), step=1, frames_per_sheet=24, thumb_width=220)
            create_consecutive_contact_sheets(path, 0, frames - 1, step=max(1, int(round(fps / 6))), frames_per_sheet=24, thumb_width=220)
        elif duration <= 22:
            create_consecutive_contact_sheets(path, 0, frames - 1, step=1, frames_per_sheet=24, thumb_width=220)
        else:
            create_consecutive_contact_sheets(path, 0, frames - 1, step=max(1, int(round(fps / 6))), frames_per_sheet=24, thumb_width=220)
    print("reference study extraction complete")
