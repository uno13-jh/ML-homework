# 新闻来源配置 - RSS feeds for finance and technology hot topics
# News source configuration for daily finance & tech digest

FINANCE_SOURCES = [
    {
        "name": "财联社",
        "url": "https://www.cls.cn/api/sw?app=rss&terminal=rss&type=hot&channel=article",
        "type": "json",
    },
    {
        "name": "36氪-财经",
        "url": "https://36kr.com/feed",
        "type": "rss",
        "keywords": ["融资", "上市", "IPO", "股市", "A股", "港股", "美股", "基金", "债券", "财经", "经济", "金融", "银行", "投资"],
    },
    {
        "name": "虎嗅网-财经",
        "url": "https://www.huxiu.com/rss/0.xml",
        "type": "rss",
        "keywords": ["融资", "上市", "IPO", "股市", "财经", "经济", "金融", "银行", "投资", "市值"],
    },
]

TECH_SOURCES = [
    {
        "name": "36氪-科技",
        "url": "https://36kr.com/feed",
        "type": "rss",
        "keywords": ["AI", "人工智能", "芯片", "大模型", "科技", "互联网", "云计算", "自动驾驶", "机器人", "量子"],
    },
    {
        "name": "虎嗅网-科技",
        "url": "https://www.huxiu.com/rss/0.xml",
        "type": "rss",
        "keywords": ["AI", "人工智能", "芯片", "大模型", "科技", "互联网", "云计算", "自动驾驶", "机器人", "手机"],
    },
    {
        "name": "IT之家",
        "url": "https://www.ithome.com/rss/",
        "type": "rss",
        "keywords": [],  # all articles are tech-related
    },
    {
        "name": "少数派",
        "url": "https://sspai.com/feed",
        "type": "rss",
        "keywords": [],
    },
]

# 备用：知名财经科技媒体 RSS（英文，用于补充）
BACKUP_SOURCES = [
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "type": "rss",
        "keywords": [],
        "lang": "en",
    },
    {
        "name": "Reuters Technology",
        "url": "https://feeds.reuters.com/reuters/technologyNews",
        "type": "rss",
        "keywords": [],
        "lang": "en",
    },
]
