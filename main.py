import os, sys, json, hashlib, datetime, requests

"""
NULL — Channel 0 (Пустота) Autoposter
Slots: atmo1, atmo2, challenge, cta
Rotation: by day-of-year + deterministic salt per slot -> no near repeats.
Secrets (GitHub):
  - BOT_TOKEN
  - CHANNEL_ID   (e.g., @your_channel or numeric id)
  - BOT_LINK     (for CTA templates: [BOT_LINK])
"""

API_URL = "https://api.telegram.org/bot{token}/sendMessage"

def deterministic_index(pool_len: int, slot: str, day_of_year: int) -> int:
    h = hashlib.md5(slot.encode("utf-8")).digest()
    salt = int.from_bytes(h[:2], "big")
    return (day_of_year + salt) % pool_len

def load_templates(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for key in ["atmo", "challenge", "cta"]:
        if key not in data or not isinstance(data[key], list) or not data[key]:
            raise ValueError(f"templates.json: missing or empty '{key}' list")
    return data

def render_text(slot: str, phrase: str, bot_link: str | None) -> str:
    if slot.startswith("atmo"):
        return f"{phrase}"
    if slot == "challenge":
        return f"⦿ {phrase}"
    if slot == "cta":
        link = bot_link or ""
        return phrase.replace("{link}", link)
    return phrase

def post(token: str, chat_id: str, text: str):
    resp = requests.post(
        API_URL.format(token=token),
        json={
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": True
        },
        timeout=20
    )
    if not resp.ok:
        raise SystemExit(f"Telegram API error: {resp.status_code} {resp.text}")
    return resp.json()

def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python main.py <slot: atmo1|atmo2|challenge|cta>")
    slot = sys.argv[1].strip().lower()
    if slot not in {"atmo1", "atmo2", "challenge", "cta"}:
        raise SystemExit("Invalid slot. Use: atmo1, atmo2, challenge, cta")

    token = os.environ.get("BOT_TOKEN", "").strip()
    chat_id = os.environ.get("CHANNEL_ID", "").strip()
    bot_link = os.environ.get("BOT_LINK", "").strip()

    if not token or not chat_id:
        raise SystemExit("Missing BOT_TOKEN or CHANNEL_ID env")

    templates = load_templates("templates.json")
    day_of_year = int(datetime.datetime.utcnow().strftime("%j"))

    if slot in {"atmo1", "atmo2"}:
        pool = templates["atmo"]
    elif slot == "challenge":
        pool = templates["challenge"]
    else:
        pool = templates["cta"]

    idx = deterministic_index(len(pool), slot, day_of_year)
    phrase = pool[idx]
    text = render_text(slot, phrase, bot_link)
    data = post(token, chat_id, text)
    print("Posted:", data.get("result", {}).get("message_id"))

if __name__ == "__main__":
    main()
