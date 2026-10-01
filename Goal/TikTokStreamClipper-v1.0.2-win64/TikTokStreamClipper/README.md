# TikTok Stream Clipper

[![⬇ Download the app](https://img.shields.io/badge/%E2%AC%87%20Download%20the%20app-Windows%20.exe-2ea44f?style=for-the-badge)](https://github.com/Roy-Mutwiri/TIKTOKPOSTER/releases/latest)

> **⚡ Just want to run it?** [**Download the latest release**](https://github.com/Roy-Mutwiri/TIKTOKPOSTER/releases/latest),
> unzip it, and double-click **`Start-App.bat`** — the app opens in your browser.
> No Python or building needed. See **[HOW-TO-USE.md](HOW-TO-USE.md)** for the full guide.
>
> *Working from the source instead? Double-click `Start-App.bat` in the repo — it builds the app the first time, then launches it.*

This project wraps `external/TiktokAutoUploader` and adds the missing workflow for long YouTube streams:

1. Download one YouTube stream/video.
2. Slice it into 30-50 second vertical clips.
3. Generate varied trading/motivation post captions with up to 4 hashtags.
4. Upload clips to a saved TikTok account through the integrated uploader.

## Setup

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
python -m pip install -r external\TiktokAutoUploader\requirements.txt
```

Install the uploader signature dependencies:

```powershell
Push-Location external\TiktokAutoUploader\tiktok_uploader\tiktok-signature
npm install
npx playwright install chromium
Pop-Location
```

The clipper uses `ffmpeg`. If `ffmpeg` is not on `PATH`, the `imageio-ffmpeg`
package from `requirements.txt` is used automatically.

## Login

Save a TikTok session once:

```powershell
python -m tiktok_poster login --account main
```

## Web UI

Run the local interface:

```powershell
python -m tiktok_poster serve --host 127.0.0.1 --port 8787
```

Open `http://127.0.0.1:8787` in your browser.

When you paste a YouTube link, the UI analyzes the video duration and fills the
recommended clip count for the selected clip length range.

This project uses option 2 for TikTok posting: a saved browser session. On the
Upload page, use `Open TikTok`, scan the QR code or log in normally, and keep
the same account label for uploads.

## Generate Clips

Create 100 clips from a YouTube stream:

```powershell
python -m tiktok_poster generate --youtube "https://www.youtube.com/watch?v=VIDEO_ID" --count 100
```

The command writes clips under `data\clips\...` and creates a CSV manifest under `data\manifests\...`.
Review that manifest before uploading.

## Upload

Dry-run the next 5 ready posts:

```powershell
python -m tiktok_poster upload --manifest data\manifests\YOUR_BATCH.csv --account main --limit 5 --dry-run
```

Upload with the conservative human-paced defaults:

```powershell
python -m tiktok_poster upload --manifest data\manifests\YOUR_BATCH.csv --account main --limit 20
```

By default there is **no post-count limit**. Each post waits a random gap of
1-15 minutes (60-900 seconds); adjust it with `--delay-min-seconds` /
`--delay-max-seconds`. If you want a self-imposed daily cap you can still set one
with `--daily-post-cap N` (`0`, the default, means unlimited). If TikTok itself
returns a quota or rate-limit signal, the run stops immediately and keeps the
remaining clips queued instead of retrying.
