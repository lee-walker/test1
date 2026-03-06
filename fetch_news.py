import feedparser
import json

def fetch_news():
    feeds = [
        "https://www.reutersagency.com/feed/?best-sectors=international-news&post_type=best",
        "https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=finance",
        "https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    ]
    
    news_items = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            news_items.append({
                "title": entry.title,
                "link": entry.link
            })
    
    # Limit to 30 items for Gemini to process (we'll ask for 20 in the summary)
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_items[:30], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_news()
