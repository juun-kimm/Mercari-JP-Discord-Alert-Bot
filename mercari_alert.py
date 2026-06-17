import os
import json
import time
import hashlib
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]
QUERY = os.getenv("SEARCH_QUERY", "koji kuga")
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "10"))

SEEN_FILE = "seen.json"


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


def send_discord_alert(item):
    embed = {
        "title": item["title"],
        "url": item["url"],
        "description": item["price"] or "Price not found",
        "fields": [
            {
                "name": "Mercari JP",
                "value": f"[Open listing]({item['url']})",
                "inline": False,
            }
        ],
    }

    if item.get("image"):
        embed["image"] = {"url": item["image"]}

    payload = {
        "content": f"🔥 New Mercari JP listing for **{QUERY}**",
        "embeds": [embed],
    }

    r = requests.post(WEBHOOK, json=payload, timeout=15)
    r.raise_for_status()


def scrape_listings(page):
    url = (
        "https://jp.mercari.com/search"
        f"?keyword={quote(QUERY)}"
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

        title = "Mercari listing"
        price = ""

        for line in lines:
            if "¥" in line or "円" in line or "US$" in line:
                price = line
            elif title == "Mercari listing":
                title = line

        image = ""
        img = card.locator("img").first
        if img.count() > 0:
            image = img.get_attribute("src") or ""

        results.append(
            {
                "id": listing_id_from_url(full_url),
                "title": title,
                "price": price,
                "url": full_url,
                "image": image,
            }
        )

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

        print(f"Watching Mercari JP for: {QUERY}")
        print(f"Polling every {POLL_SECONDS} seconds")

        while True:
            try:
                listings = scrape_listings(page)
                print(f"Checked {len(listings)} listings")

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