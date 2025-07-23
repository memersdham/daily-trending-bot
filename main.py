import os
import requests
from bs4 import BeautifulSoup
import feedparser

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, data=data)
        print("Telegram status:", response.status_code)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Failed to send:", e)

def get_google_trends():
    try:
        print("Fetching Google Trends...")
        feed = feedparser.parse("https://trends.google.com/trends/trendingsearches/daily/rss?geo=US")
        if not feed.entries:
            raise Exception("Empty RSS feed")
        items = feed.entries[:10]
        results = [f"- {item.title}" for item in items]
        return "*📈 Google Trends (US):*\n" + "\n".join(results)
    except Exception as e:
        print("Google Trends error:", e)
        return "*📈 Google Trends (US):*\n- No data available."

def get_reddit_trending():
    try:
        print("Fetching Reddit Popular...")
        headers = {'User-agent': 'Mozilla/5.0'}
        res = requests.get("https://old.reddit.com/r/popular/", headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        titles = soup.select("div.thing > div.entry > p.title > a")[:10]
        if not titles:
            raise Exception("No titles found")
        return "*🔺 Reddit Popular:*\n" + "\n".join(f"- {t.text.strip()}" for t in titles)
    except Exception as e:
        print("Reddit error:", e)
        return "*🔺 Reddit Popular:*\n- No data available."

def get_instagram_hashtags():
    try:
        print("Fetching Instagram Hashtags...")
        url = "https://inbeat.co/instagram-trending-hashtags/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        tags = soup.select("a.tag")[:10]
        if not tags:
            raise Exception("No tags found")
        hashtags = [f"- [{t.text.strip()}](https://www.instagram.com/explore/tags/{t.text.strip().replace('#', '')}/)" for t in tags]
        return "*📊 Instagram Trending Hashtags:*\n" + "\n".join(hashtags)
    except Exception as e:
        print("Instagram error:", e)
        return "*📊 Instagram Trending Hashtags:*\n- No data available."

def get_billboard_top_10():
    try:
        print("Fetching Billboard...")
        url = "https://www.billboard.com/charts/hot-100/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        songs = soup.select("li.o-chart-results-list__item h3")[:10]
        results = [f"- {s.get_text(strip=True)}" for s in songs]
        return "*🎵 Billboard Hot 100:*\n" + "\n".join(results)
    except Exception as e:
        print("Billboard error:", e)
        return "*🎵 Billboard Hot 100:*\n- No data available."

def get_imdb_trending():
    try:
        print("Fetching IMDb Movies...")
        url = "https://www.imdb.com/chart/moviemeter/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        movies = soup.select("td.titleColumn a")[:10]
        results = [f"- {m.text.strip()}" for m in movies]
        return "*🎬 IMDb Trending Movies:*\n" + "\n".join(results)
    except Exception as e:
        print("IMDb error:", e)
        return "*🎬 IMDb Trending Movies:*\n- No data available."

def send_daily_digest():
    sections = [
        get_google_trends(),
        get_reddit_trending(),
        get_instagram_hashtags(),
        get_billboard_top_10(),
        get_imdb_trending()
    ]
    full_message = "\n\n".join(sections)
    print("Sending message to Telegram...")
    send_to_telegram(full_message)

send_daily_digest()
