import feedparser
def news_signal(stock):
    feed = feedparser.parse(f"https://news.google.com/rss/search?q={stock}")
    return "🟢 Positive News" if len(feed.entries)>0 else "No news"
