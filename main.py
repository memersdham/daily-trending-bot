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
        requests.post(url, data=data)
    except Exception as e:
        print("Failed to send:", e)

def get_google_trends():
    try:
        feed = feedparser.parse("https://trends.google.com/trends/trendingsearches/daily/rss?geo=US")
        items = feed.entries[:10]
        results = [f"- {item.title}" for item in items]
        return "*📈 Google Trends (US):*\n" + "\n".join(results)
    except Exception as e:
        return f"*📈 Google Trends (US):*\n- Failed to fetch. ({e})"

def get_reddit_trending():
    try:
        headers = {'User-agent': 'Mozilla/5.0'}
        res = requests.get("https://old.reddit.com/r/popular/", headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        titles = soup.select("div.thing > div.entry > p.title > a")[:10]
        return "*🔺 Reddit Popular:*\n" + "\n".join(f"- {t.text.strip()}" for t in titles)
    except Exception as e:
        return f"*🔺 Reddit Popular:*\n- Failed to fetch. ({e})"

def get_instagram_hashtags():
    try:
        url = "https://inbeat.co/instagram-trending-hashtags/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        tags = soup.select("a.tag")[:10]
        hashtags = [f"- [{t.text.strip()}](https://www.instagram.com/explore/tags/{t.text.strip().replace('#', '')}/)" for t in tags]
        return "*📊 Instagram Trending Hashtags:*\n" + "\n".join(hashtags)
    except Exception as e:
        return f"*📊 Instagram Trending Hashtags:*\n- Failed to fetch. ({e})"

def get_billboard_top_10():
    try:
        url = "https://www.billboard.com/charts/hot-100/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        songs = soup.select("li.o-chart-results-list__item h3")[:10]
        results = [f"- {s.get_text(strip=True)}" for s in songs]
        return "*🎵 Billboard Hot 100:*\n" + "\n".join(results)
    except Exception as e:
        return f"*🎵 Billboard Hot 100:*\n- Failed to fetch. ({e})"

def get_imdb_trending():
    try:
        url = "https://www.imdb.com/chart/moviemeter/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        movies = soup.select("td.titleColumn a")[:10]
        results = [f"- {m.text.strip()}" for m in movies]
        return "*🎬 IMDb Trending Movies:*\n" + "\n".join(results)
    except Exception as e:
        return f"*🎬 IMDb Trending Movies:*\n- Failed to fetch. ({e})"

def send_daily_digest():
    sections = [
        get_google_trends(),
        get_reddit_trending(),
        get_instagram_hashtags(),
        get_billboard_top_10(),
        get_imdb_trending()
    ]
    full_message = "\n\n".join(sections)
    send_to_telegram(full_message)

send_daily_digest()
