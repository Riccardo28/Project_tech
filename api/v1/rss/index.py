from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import httpx
import feedparser
import asyncio

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            response = asyncio.run(self.get_rss_feed(query_params))
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            error = {"total": 0, "articles": [], "error": str(e)}
            self.wfile.write(json.dumps(error).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    async def get_rss_feed(self, params):
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
