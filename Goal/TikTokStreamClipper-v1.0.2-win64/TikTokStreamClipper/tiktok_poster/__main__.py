from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .pipeline import (
    DEFAULT_DAILY_POST_CAP,
    DEFAULT_DELAY_MAX_SECONDS,
    DEFAULT_DELAY_MIN_SECONDS,
    DEFAULT_STARTER_DELAY_MAX_SECONDS,
    DEFAULT_STARTER_DELAY_MIN_SECONDS,
    generate_from_youtube,
    login,
    manifest_summary,
    upload_manifest,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m tiktok_poster")
    sub = parser.add_subparsers(dest="command", required=True)

    login_cmd = sub.add_parser("login", help="Save TikTok cookies for an account")
    login_cmd.add_argument("--account", required=True, help="Local account label, e.g. main")

    gen = sub.add_parser("generate", help="Download a YouTube video and create TikTok clips")
    gen.add_argument("--youtube", required=True, help="YouTube stream/video URL")
    gen.add_argument("--count", type=int, default=100, help="Number of clips to create")
    gen.add_argument("--min-seconds", type=int, default=30)
    gen.add_argument("--max-seconds", type=int, default=50)
    gen.add_argument("--max-hashtags", type=int, default=4)
    gen.add_argument("--render-mode", choices=["chart_face", "face_only"], default="chart_face")
    gen.add_argument("--seed", type=int, default=42)

    up = sub.add_parser("upload", help="Upload clips from a manifest CSV")
    up.add_argument("--manifest", required=True, type=Path)
    up.add_argument("--account", required=True)
    up.add_argument("--limit", type=int, default=None)
    up.add_argument("--delay-seconds", type=int, default=DEFAULT_DELAY_MIN_SECONDS, help="Fallback delay between uploads")
    up.add_argument("--delay-min-seconds", type=int, default=None)
    up.add_argument("--delay-max-seconds", type=int, default=None)
    up.add_argument("--starter-count", type=int, default=0)
    up.add_argument("--starter-delay-min-seconds", type=int, default=DEFAULT_STARTER_DELAY_MIN_SECONDS)
    up.add_argument("--starter-delay-max-seconds", type=int, default=DEFAULT_STARTER_DELAY_MAX_SECONDS)
    up.add_argument("--daily-post-cap", type=int, default=DEFAULT_DAILY_POST_CAP, help="0 = unlimited (no self-imposed cap)")
    up.add_argument("--dry-run", action="store_true")

    summary = sub.add_parser("summary", help="Show manifest status counts")
    summary.add_argument("--manifest", required=True, type=Path)

    serve = sub.add_parser("serve", help="Run the local web UI")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8787)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "login":
        return login(args.account)
    if args.command == "generate":
        manifest = generate_from_youtube(
            youtube_url=args.youtube,
            count=args.count,
            min_seconds=args.min_seconds,
            max_seconds=args.max_seconds,
            seed=args.seed,
            max_hashtags=args.max_hashtags,
            render_mode=args.render_mode,
        )
        print(f"Manifest written: {manifest}")
        return 0
    if args.command == "upload":
        upload_manifest(
            args.manifest,
            args.account,
            args.limit,
            args.delay_seconds,
            args.dry_run,
            delay_min_seconds=args.delay_min_seconds,
            delay_max_seconds=args.delay_max_seconds,
            starter_count=args.starter_count,
            starter_delay_min_seconds=args.starter_delay_min_seconds,
            starter_delay_max_seconds=args.starter_delay_max_seconds,
            daily_post_cap=args.daily_post_cap,
        )
        return 0
    if args.command == "summary":
        print(json.dumps(manifest_summary(args.manifest), indent=2))
        return 0
    if args.command == "serve":
        from .web import run

        run(args.host, args.port)
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
