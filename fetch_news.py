import feedparser
import json

def fetch_news():
    feeds = [
        "https://www.reutersagency.com/feed/?best-sectors=international-news&post_type=best",
        "https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=finance",
        "https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
        "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://openai.com/news/rss.xml",
        "https://www.bleepingcomputer.com/feed/",
        "https://thehackernews.com/feeds/posts/default",
        "https://arstechnica.com/feed/",
        "https://wired.com/feed/rss"
    ]
    
    news_items = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            if feed.bozo:
                print(f"Warning: Issue parsing {url}")
            for entry in feed.entries[:10]:
                news_items.append({
                    "title": entry.title,
                    "link": entry.link
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
    # Limit to 50 items for Gemini to process
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_items[:50], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_news()
