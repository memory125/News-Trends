# coding=utf-8
"""
国际新闻获取器模块

负责从国际新闻媒体获取数据，支持：
- Twitter/X 热门话题
- YouTube 新闻视频
- BBC News
- Reuters
- CNN International
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime

import requests


class InternationalNewsFetcher:
    """国际新闻获取器"""

    def __init__(self, proxy_url: Optional[str] = None):
        """
        初始化国际新闻获取器

        Args:
            proxy_url: 代理服务器 URL（可选）
        """
        self.proxy_url = proxy_url
        self.session = requests.Session()

    def fetch_twitter_hashtag(self, hashtag: str, url: str) -> List[Dict]:
        """
        获取 Twitter/X 热门话题数据

        Args:
            hashtag: 话题标签（如 #Iran）
            url: Twitter 搜索 URL

        Returns:
            新闻列表
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            proxies = None
            if self.proxy_url:
                proxies = {"http": self.proxy_url, "https": self.proxy_url}

            response = self.session.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=15,
            )
            response.raise_for_status()

            # 注意：Twitter 需要登录才能看到完整内容，这里返回基础信息
            news_items = []
            if "twitter.com" in url:
                # 模拟 Twitter 热门话题数据（实际需要从 API 获取）
                news_items.append({
                    "title": f"{hashtag} - Latest Updates",
                    "url": url,
                    "source": "Twitter/X",
                    "timestamp": datetime.now().isoformat(),
                    "type": "twitter_hashtag"
                })

            return news_items

        except Exception as e:
            print(f"获取 Twitter 数据失败：{e}")
            return []

    def fetch_youtube_search(self, query: str, url: str) -> List[Dict]:
        """
        获取 YouTube 搜索结果

        Args:
            query: 搜索关键词
            url: YouTube 搜索 URL

        Returns:
            视频列表
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            proxies = None
            if self.proxy_url:
                proxies = {"http": self.proxy_url, "https": self.proxy_url}

            response = self.session.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=15,
            )
            response.raise_for_status()

            # 注意：YouTube 需要解析 HTML 获取视频列表，这里返回基础信息
            news_items = []
            if "youtube.com" in url:
                news_items.append({
                    "title": f"{query} - Video Results",
                    "url": url,
                    "source": "YouTube",
                    "timestamp": datetime.now().isoformat(),
                    "type": "youtube_search"
                })

            return news_items

        except Exception as e:
            print(f"获取 YouTube 数据失败：{e}")
            return []

    def fetch_bbc_news(self, category: str, url: str) -> List[Dict]:
        """
        获取 BBC News 报道

        Args:
            category: 新闻分类（如 world-middle-east）
            url: BBC 新闻 URL

        Returns:
            新闻列表
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            proxies = None
            if self.proxy_url:
                proxies = {"http": self.proxy_url, "https": self.proxy_url}

            response = self.session.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=15,
            )
            response.raise_for_status()

            # 注意：BBC 需要解析 HTML 获取新闻列表，这里返回基础信息
            news_items = []
            if "bbc.com" in url:
                news_items.append({
                    "title": f"BBC News - {category.replace('-', ' ').title()}",
                    "url": url,
                    "source": "BBC News",
                    "timestamp": datetime.now().isoformat(),
                    "type": "bbc_news"
                })

            return news_items

        except Exception as e:
            print(f"获取 BBC 数据失败：{e}")
            return []

    def fetch_reuters_news(self, category: str, url: str) -> List[Dict]:
        """
        获取 Reuters 新闻

        Args:
            category: 新闻分类（如 middle-east）
            url: Reuters 新闻 URL

        Returns:
            新闻列表
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            proxies = None
            if self.proxy_url:
                proxies = {"http": self.proxy_url, "https": self.proxy_url}

            response = self.session.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=15,
            )
            response.raise_for_status()

            # 注意：Reuters 需要解析 HTML 获取新闻列表，这里返回基础信息
            news_items = []
            if "reuters.com" in url:
                news_items.append({
                    "title": f"Reuters - {category.replace('-', ' ').title()} News",
                    "url": url,
                    "source": "Reuters",
                    "timestamp": datetime.now().isoformat(),
                    "type": "reuters_news"
                })

            return news_items

        except Exception as e:
            print(f"获取 Reuters 数据失败：{e}")
            return []

    def fetch_cnn_news(self, category: str, url: str) -> List[Dict]:
        """
        获取 CNN International 新闻

        Args:
            category: 新闻分类（如 world）
            url: CNN 新闻 URL

        Returns:
            新闻列表
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            proxies = None
            if self.proxy_url:
                proxies = {"http": self.proxy_url, "https": self.proxy_url}

            response = self.session.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=15,
            )
            response.raise_for_status()

            # 注意：CNN 需要解析 HTML 获取新闻列表，这里返回基础信息
            news_items = []
            if "cnn.com" in url:
                news_items.append({
                    "title": f"CNN International - {category.replace('-', ' ').title()} News",
                    "url": url,
                    "source": "CNN International",
                    "timestamp": datetime.now().isoformat(),
                    "type": "cnn_news"
                })

            return news_items

        except Exception as e:
            print(f"获取 CNN 数据失败：{e}")
            return []

    def fetch_website(self, category: str, url: str) -> List[Dict]:
        """
        抓取网站新闻（Wired, The Verge, Bloomberg, CNBC 等）

        Args:
            category: 分类（technology, business, finance 等）
            url: 网站 URL

        Returns:
            新闻列表
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            proxies = None
            if self.proxy_url:
                proxies = {"http": self.proxy_url, "https": self.proxy_url}

            response = self.session.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=15,
            )
            response.raise_for_status()

            # 注意：需要解析 HTML 获取新闻列表，这里返回基础信息
            news_items = []
            if "wired.com" in url:
                news_items.append({
                    "title": f"Wired - {category.title()} News",
                    "url": url,
                    "source": "Wired Magazine",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })
            elif "theverge.com" in url:
                news_items.append({
                    "title": f"The Verge - {category.title()} News",
                    "url": url,
                    "source": "The Verge",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })
            elif "arstechnica.com" in url:
                news_items.append({
                    "title": f"Ars Technica - {category.title()} News",
                    "url": url,
                    "source": "Ars Technica",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })
            elif "bloomberg.com" in url:
                news_items.append({
                    "title": f"Bloomberg - {category.title()} News",
                    "url": url,
                    "source": "Bloomberg News",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })
            elif "cnbc.com" in url:
                news_items.append({
                    "title": f"CNBC - {category.title()} News",
                    "url": url,
                    "source": "CNBC",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })
            elif "ft.com" in url:
                news_items.append({
                    "title": f"Financial Times - {category.title()} News",
                    "url": url,
                    "source": "Financial Times",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })
            elif "wsj.com" in url:
                news_items.append({
                    "title": f"Wall Street Journal - {category.title()} News",
                    "url": url,
                    "source": "Wall Street Journal",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })
            elif "venturebeat.com/ai" in url:
                news_items.append({
                    "title": f"VentureBeat AI - Artificial Intelligence News",
                    "url": url,
                    "source": "VentureBeat AI",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })
            elif "technologyreview.com" in url:
                news_items.append({
                    "title": f"MIT Technology Review - Emerging Tech News",
                    "url": url,
                    "source": "MIT Technology Review",
                    "timestamp": datetime.now().isoformat(),
                    "type": "website"
                })

            return news_items

        except Exception as e:
            print(f"抓取网站数据失败：{e}")
            return []

    def fetch_all_international(self, sources: List[Dict]) -> Dict[str, List[Dict]]:
        """
        批量获取所有国际新闻源数据

        Args:
            sources: 配置的国际新闻源列表

        Returns:
            结果字典 {platform_id: [news_items]}
        """
        results = {}

        for source in sources:
            platform_id = source.get("id")
            news_type = source.get("type")

            try:
                if news_type == "twitter_hashtag":
                    hashtag = source.get("hashtag", "#News")
                    url = source.get("url", "")
                    results[platform_id] = self.fetch_twitter_hashtag(hashtag, url)

                elif news_type == "youtube_search":
                    query = source.get("query", "news")
                    url = source.get("url", "")
                    results[platform_id] = self.fetch_youtube_search(query, url)

                elif news_type == "bbc_news":
                    category = source.get("category", "world")
                    url = source.get("url", "")
                    results[platform_id] = self.fetch_bbc_news(category, url)

                elif news_type == "reuters_news":
                    category = source.get("category", "world")
                    url = source.get("url", "")
                    results[platform_id] = self.fetch_reuters_news(category, url)

                elif news_type == "cnn_news":
                    category = source.get("category", "world")
                    url = source.get("url", "")
                    results[platform_id] = self.fetch_cnn_news(category, url)

                elif news_type == "website":
                    category = source.get("category", "technology")
                    url = source.get("url", "")
                    results[platform_id] = self.fetch_website(category, url)

            except Exception as e:
                print(f"获取 {platform_id} 数据失败：{e}")
                results[platform_id] = []

            # 请求间隔（避免过快）
            time.sleep(1)

        return results
