from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import httpx
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
            response = asyncio.run(self.get_hacker_news(query_params))
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

    async def get_hacker_news(self, params):
        try:
            limit = int(params.get('limit', ['10'])[0])
            story_type = params.get('story_type', ['topstories'])[0]

            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"https://hacker-news.firebaseio.com/v0/{story_type}.json"
                response = await client.get(url)
                story_ids = response.json()[:limit * 2]

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
