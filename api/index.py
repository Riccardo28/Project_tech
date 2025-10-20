from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import httpx
import feedparser
import asyncio

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

        try:
            # Route handling
            if path == '/api' or path == '/api/':
                response = {"message": "Tech News Hub API", "status": "online"}
            elif path == '/api/health':
                response = {"status": "healthy"}
            elif path.startswith('/api/v1/hacker-news'):
                response = asyncio.run(self.get_hacker_news(query_params))
            elif path.startswith('/api/v1/rss'):
                response = asyncio.run(self.get_rss_feed(query_params))
            else:
                response = {"error": "Not found"}

            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    async def get_hacker_news(self, params):
        """Fetch Hacker News articles"""
        try:
            limit = int(params.get('limit', ['10'])[0])
            story_type = params.get('story_type', ['topstories'])[0]

            async with httpx.AsyncClient(timeout=10.0) as client:
                # Fetch story IDs
                url = f"https://hacker-news.firebaseio.com/v0/{story_type}.json"
                response = await client.get(url)
                story_ids = response.json()[:limit * 2]

                # Fetch articles
                articles = []
                for story_id in story_ids:
                    try:
                        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                        item_response = await client.get(item_url)
                        data = item_response.json()

                        if data and data.get("type") == "story":
                            articles.append({
                                "id": data.get("id"),
                                "title": data.get("title"),
                                "url": data.get("url"),
                                "score": data.get("score", 0),
                                "by": data.get("by"),
                                "time": data.get("time"),
                                "descendants": data.get("descendants", 0),
                                "type": data.get("type")
                            })

                            if len(articles) >= limit:
                                break
                    except:
                        continue

                return {"total": len(articles), "articles": articles}
        except Exception as e:
            return {"total": 0, "articles": [], "error": str(e)}

    async def get_rss_feed(self, params):
        """Fetch RSS feed"""
        try:
            url = params.get('url', [None])[0]
            if not url:
                return {"total": 0, "articles": [], "error": "URL parameter required"}

            limit = int(params.get('limit', ['20'])[0])

            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url)
                content = response.text

            feed = feedparser.parse(content)
            articles = []

            for entry in feed.entries[:limit]:
                try:
                    articles.append({
                        "title": entry.get('title', 'No Title'),
                        "link": entry.get('link'),
                        "description": entry.get('summary') or entry.get('description'),
                        "summary": entry.get('summary'),
                        "published": entry.get('published') or entry.get('updated'),
                        "author": entry.get('author'),
                        "guid": entry.get('id') or entry.get('link')
                    })
                except:
                    continue

            return {"total": len(articles), "articles": articles}
        except Exception as e:
            return {"total": 0, "articles": [], "error": str(e)}
