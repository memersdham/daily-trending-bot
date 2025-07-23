import os
import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq

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
        pytrends = TrendReq(hl='en-US', tz=360)
        trending = pytrends.trending_searches(pn='united_states')
        top = trending[0].tolist()[:10]
        return "*📈 Google Trends (US):*\n" + "\n".join(f"- {x}" for x in top)
    except:
        return "*📈 Google Trends (US):*\n- Failed to fetch."

def get_reddit_trending():
    try:
        headers = {'User-agent': 'Mozilla/5.0'}
        res = requests.get("https://www.reddit.com/r/popular.json", headers=headers)
        posts = res.json()["data"]["children"][:10]
        return "*🔺 Reddit Popular:*\n" + "\n".join(f"- {p['data']['title']}" for p in posts)
    except:
        return "*🔺 Reddit Popular:*\n- Failed to fetch."

def get_instagram_hashtags():
    try:
        url = "https://inbeat.co/instagram-trending-hashtags/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        tags = soup.select("a.tag")[:10]
        hashtags = [f"- [{t.text.strip()}](https://www.instagram.com/explore/tags/{t.text.strip().replace('#', '')}/)" for t in tags]
        return "*📊 Instagram Trending Hashtags:*\n" + "\n".join(hashtags)
    except:
        return "*📊 Instagram Trending Hashtags:*\n- Failed to fetch."

def get_billboard_top_10():
    try:
        url = "https://www.billboard.com/charts/hot-100/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        titles = soup.select("li.o-chart-results-list__item h3")[:10]
        songs = [f"- {title.get_text(strip=True)}" for title in titles]
        return "*🎵 Billboard Hot 100:*\n" + "\n".join(songs)
    except:
        return "*🎵 Billboard Hot 100:*\n- Failed to fetch."

def get_imdb_trending():
    try:
        url = "https://www.imdb.com/chart/moviemeter/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        movies = soup.select("td.titleColumn a")[:10]
        trending = [f"- {m.text}" for m in movies]
        return "*🎬 IMDb Trending Movies:*\n" + "\n".join(trending)
    except:
        return "*🎬 IMDb Trending Movies:*\n- Failed to fetch."

def send_daily_digest():
    content = "\n\n".join([
        get_google_trends(),
        get_reddit_trending(),
        get_instagram_hashtags(),
        get_billboard_top_10(),
        get_imdb_trending()
    ])
    send_to_telegram(content)

send_daily_digest()
