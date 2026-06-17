import os
import re
import json
import time
import hashlib
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]
QUERIES = [q.strip() for q in os.getenv("SEARCH_QUERY", "koji kuga").split(",") if q.strip()]
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "10"))

SEEN_FILE = "seen.json"

PRICE_PATTERNS = [
    r"US\$\s*[\d,]+(?:\.\d+)?",
    r"[\d,]+(?:\.\d+)?\s*US\$",
    r"\$\s*[\d,]+(?:\.\d+)?",
    r"¥\s*[\d,]+",
    r"[\d,]+(?:\.\d+)?\s*円",
]


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, ensure_ascii=False, indent=2)


def listing_id_from_url(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def looks_like_price(text):
    t = text.strip()
    if re.search(r"¥|円|US\$|\$", t):
        return True
    if re.fullmatch(r"[\d,]+(?:\.\d+)?", t):
        return True
    return False


def extract_price(text):
    flat = " ".join(text.split())

    for pat in PRICE_PATTERNS:
        m = re.search(pat, flat)
        if not m:
            continue

        raw = m.group(0)
        num = re.search(r"[\d,]+(?:\.\d+)?", raw)

        if not num:
            return raw.strip()

        if "US$" in raw or "$" in raw:
            return f"${float(num.group(0).replace(',', '')):,.2f}"

        if "¥" in raw:
            return f"¥{num.group(0)}"

        if "円" in raw:
            return f"{num.group(0)}円"

    return ""


def extract_title(card, lines):
    label = card.get_attribute("aria-label")
    if label and label.strip() and not looks_like_price(label.strip()):
        return label.strip()

    img = card.locator("img").first
    if img.count() > 0:
        alt = img.get_attribute("alt")
        if alt and alt.strip() and not looks_like_price(alt.strip()):
            return alt.strip()

    for line in lines:
        if not looks_like_price(line):
            return line

    return "Mercari listing"


def send_discord_alert(item):
    embed = {
        "title": item["title"],
        "url": item["url"],
        "description": f"**Price:** {item['price'] or 'Price not found'}",
    }

    if item.get("image"):
        embed["image"] = {"url": item["image"]}

    payload = {
        "content": f"🔥 New Mercari JP listing for **{item['query']}**",
        "embeds": [embed],
    }

    r = requests.post(WEBHOOK, json=payload, timeout=15)
    r.raise_for_status()


def scrape_listings(page, query):
    url = (
        "https://jp.mercari.com/search"
        f"?keyword={quote(query)}"
        "&sort=created_time"
        "&order=desc"
    )

    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(5000)

    cards = page.locator('a[href^="/item/"]').all()
    results = []

    for card in cards[:40]:
        href = card.get_attribute("href")
        if not href:
            continue

        full_url = "https://jp.mercari.com" + href.split("?")[0]

        text = card.inner_text().strip()
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        img = card.locator("img").first
        image = img.get_attribute("src") if img.count() > 0 else ""

        results.append({
            "id": listing_id_from_url(full_url),
            "query": query,
            "title": extract_title(card, lines),
            "price": extract_price(text),
            "url": full_url,
            "image": image or "",
        })

    return results


def main():
    seen = load_seen()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            locale="ja-JP",
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            ),
        )

        page = context.new_page()

        print(f"Watching Mercari JP for: {', '.join(QUERIES)}")
        print(f"Polling every {POLL_SECONDS} seconds")

        while True:
            try:
                for query in QUERIES:
                    listings = scrape_listings(page, query)
                    print(f"Checked {len(listings)} listings for: {query}")

                    for item in reversed(listings):
                        if item["id"] not in seen:
                            print(f"New: {item['title']} | {item['price']} | {item['url']}")
                            send_discord_alert(item)
                            seen.add(item["id"])
                            save_seen(seen)
                            time.sleep(1)

            except KeyboardInterrupt:
                print("Stopped.")
                break

            except Exception as e:
                print("Error:", repr(e))

            time.sleep(POLL_SECONDS)

        browser.close()


if __name__ == "__main__":
    main()
