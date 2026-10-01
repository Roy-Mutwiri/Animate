from __future__ import annotations

import json
import random
import re
from pathlib import Path


HOOKS = [
    "Trading discipline beats impulse every time.",
    "One clean setup is better than forcing ten bad trades.",
    "Risk management is the real edge.",
    "Patience pays more than prediction.",
    "Trade the plan, not the emotion.",
    "The best traders protect capital first.",
    "Your next level starts with better habits.",
    "Consistency is built one decision at a time.",
    "Focus on process before profit.",
    "Small wins compound when discipline stays consistent.",
    "Most traders lose focus before they lose money.",
    "The setup matters less than the discipline behind it.",
    "A calm trader sees the move before the crowd reacts.",
    "Protecting capital is how confidence compounds.",
]

CAPTION_TEMPLATES = [
    "{hook} Save this reminder before your next session.",
    "{hook} The chart rewards patience, not panic.",
    "{hook} Keep your entries intentional and your risk defined.",
    "{hook} This is the mindset shift most traders ignore.",
    "{hook} Build the habit before chasing the result.",
    "{hook} A strong setup does not need emotional execution.",
    "{hook} Let the market come to your level.",
    "{hook} Protect your focus and protect your account.",
    "{hook} Watch the reaction, not the noise.",
    "{hook} This is the part most traders skip.",
    "{hook} Small rules create big consistency.",
    "{hook} The boring habits are usually the profitable ones.",
]

HASHTAGS = [
    "trading", "daytrading", "forextrading", "stockmarket", "tradingtips",
    "tradingpsychology", "riskmanagement", "priceaction", "technicalanalysis",
    "futures", "futurestrading", "nasdaq", "nq", "marketanalysis", "chartanalysis",
    "investing", "investment", "investor", "investingtips", "longterminvesting",
    "money", "wealth", "wealthbuilding", "financialfreedom", "financialeducation",
    "personalfinance", "cashflow", "passiveincome", "entrepreneurship", "business",
    "motivation", "discipline", "mindset", "successmindset", "growthmindset",
    "millionairemindset", "moneytok", "financetok", "tradingtok", "wealthtok",
    "personalfinancetips", "investingforbeginners", "learnwithtiktok",
    "trusttheprocess", "onthisday", "trending", "viral",
]

HASHTAG_BUCKETS = [
    ["trading", "daytrading", "tradingtips", "futurestrading", "priceaction", "technicalanalysis", "tradingtok"],
    ["investing", "investment", "investingtips", "stockmarket", "marketanalysis", "chartanalysis", "investingforbeginners"],
    ["money", "wealth", "wealthbuilding", "financialfreedom", "personalfinance", "personalfinancetips", "cashflow"],
    ["motivation", "discipline", "mindset", "successmindset", "growthmindset", "millionairemindset", "trusttheprocess"],
    ["moneytok", "financetok", "wealthtok", "entrepreneurship", "business", "learnwithtiktok", "onthisday", "trending", "viral"],
]


def _custom_trending_hashtags() -> list[str]:
    path = Path(__file__).resolve().parents[1] / "data" / "trending_hashtags.json"
    if not path.exists():
        return []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    raw_tags = value.get("hashtags", value) if isinstance(value, dict) else value
    if not isinstance(raw_tags, list):
        return []
    tags: list[str] = []
    for item in raw_tags:
        tag = re.sub(r"[^A-Za-z0-9]", "", str(item).lstrip("#"))
        if tag and tag.lower() not in {existing.lower() for existing in tags}:
            tags.append(tag)
    return tags[:40]


def mixed_hashtags(rng: random.Random, max_hashtags: int) -> list[str]:
    limit = max(1, min(max_hashtags, 4))
    tags: list[str] = []
    core_buckets = HASHTAG_BUCKETS[:4]
    discovery_bucket = _custom_trending_hashtags() or HASHTAG_BUCKETS[4]
    rng.shuffle(core_buckets)
    for bucket in core_buckets[: max(0, limit - 1)]:
        candidates = [tag for tag in bucket if tag not in tags]
        if candidates:
            tags.append(rng.choice(candidates))
        if len(tags) >= limit:
            break
    if len(tags) < limit:
        candidates = [tag for tag in discovery_bucket if tag not in tags]
        if candidates:
            tags.append(rng.choice(candidates))
    while len(tags) < limit:
        candidate = rng.choice(HASHTAGS)
        if candidate not in tags:
            tags.append(candidate)
    rng.shuffle(tags)
    return tags


def make_caption(index: int, rng: random.Random, max_hashtags: int = 4) -> str:
    """Create a varied TikTok caption with a fixed hashtag count."""
    hook = HOOKS[index % len(HOOKS)]
    template = rng.choice(CAPTION_TEMPLATES)
    tags = mixed_hashtags(rng, max_hashtags)
    return f"{template.format(hook=hook)} " + " ".join(f"#{tag}" for tag in tags)
