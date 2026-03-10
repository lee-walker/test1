import feedparser
import json
import socket

# 设置全局超时，防止某个 feed 卡死整个流程
socket.setdefaulttimeout(20)

def fetch_news():
    feeds = [
        # 综合新闻
        "https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
        "https://feeds.feedburner.com/solidot", # 奇客 Solidot
        "https://rsshub.app/zaobao/realtime/china", # 联合早报
        # 科技 & AI
        "https://36kr.com/feed",
        "https://sspai.com/feed",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        # 安全
        "https://thehackernews.com/feeds/posts/default",
        "https://www.bleepingcomputer.com/feed/"
    ]
    
    news_items = []
    print(f"Starting to fetch news from {len(feeds)} sources...")
    
    for url in feeds:
        try:
            # 模拟浏览器 User-Agent 避免被屏蔽
            feed = feedparser.parse(url, agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            if not feed.entries:
                print(f"Warning: No entries found for {url}")
                continue
                
            for entry in feed.entries[:8]:
                # 尽量获取摘要，如果没有则留空
                summary = getattr(entry, 'summary', '')
                if not summary and hasattr(entry, 'description'):
                    summary = entry.description
                
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": feed.feed.get('title', 'Unknown Source'),
                    "raw_summary": summary[:200] if summary else "" # 提供部分原文摘要给 Gemini 参考
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
    print(f"Total news items fetched: {len(news_items)}")
    
    # 限制 60 条，保证不超出 context 但覆盖面够广
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_items[:60], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_news()
