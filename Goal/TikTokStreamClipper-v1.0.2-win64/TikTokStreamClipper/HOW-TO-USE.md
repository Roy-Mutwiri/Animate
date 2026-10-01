# How to Use — Quick Start (No coding needed)

This app downloads a YouTube stream, cuts it into short vertical clips, writes
captions, and uploads them to TikTok. Here is the easiest way to run it.

## 1. Get the files

Download this repository (green **Code** button → **Download ZIP**) and unzip it,
**or** clone it with git. Keep all the files together in one folder.

## 2. Start the app (one double-click)

Double-click **`Start-App.bat`**.

- The first time, it builds the app for you (takes a few minutes). You need
  **Python 3.11+** installed — get it from <https://www.python.org/downloads/>
  and tick *"Add python.exe to PATH"* during setup.
- After that, it launches instantly and opens your browser at
  **http://127.0.0.1:8787**.

Keep the small black window open while you use the app. Close it to stop.

> Prefer to build once and run later? Double-click **`Build-App.bat`** to create
> `TikTokStreamClipper.exe`, then double-click **`Start-App.bat`** any time.

## 3. Use the app in your browser

| Page | What it does |
|------|--------------|
| **Generate** | Paste a YouTube link, pick how many clips, and create them |
| **Upload**   | Connect your TikTok account and post the clips |

### One-time TikTok setup for uploading

**Just double-click `Setup-Upload.bat`** once. It installs everything the
login/upload needs. You need these installed first (the script tells you if any
are missing):

- **Python 3.11+** — <https://www.python.org/downloads/> (tick *Add to PATH*)
- **Google Chrome** — <https://www.google.com/chrome/> (login opens a Chrome window)
- **Node.js LTS** — <https://nodejs.org/> (needed to sign uploads)

After setup, go to the **Upload** page, click **Open TikTok**, log in until your
TikTok home page fully loads, then close the browser. Keep the same account
label for future uploads.

> Generating and previewing clips does **not** need any of this — only logging in
> and posting to TikTok does.

## Folder guide

| File / folder | What it is |
|---------------|------------|
| **`Start-App.bat`** | ▶ Double-click to run the app |
| **`Setup-Upload.bat`** | 🔑 Double-click once to enable TikTok login/uploading |
| **`Build-App.bat`** | 🔨 Double-click to (re)build the exe |
| `TikTokStreamClipper.exe` | The app itself (created by the build) |
| `data\` | Your downloaded videos, clips, and manifests appear here |
| `web\`, `external\` | App files — leave them next to the exe |
| `tiktok_poster\` | The source code |

## Advanced (command line)

The exe is also a full CLI — run it from a terminal:

```powershell
TikTokStreamClipper.exe generate --youtube "https://youtu.be/VIDEO_ID" --count 100
TikTokStreamClipper.exe upload --manifest data\manifests\YOUR_BATCH.csv --account main --limit 20
TikTokStreamClipper.exe --help
```

## Troubleshooting

- **"Python is not installed"** → install Python 3.11+ and re-run `Build-App.bat`.
- **The app opens but pages look broken** → make sure `TikTokStreamClipper.exe`
  sits in the same folder as the `web\` and `external\` folders.
- **Nothing opens** → visit <http://127.0.0.1:8787> manually in your browser.
