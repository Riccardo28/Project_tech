from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx
import feedparser
import asyncio

# Initialize FastAPI app
app = FastAPI(title="Tech News Hub API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HackerNewsArticle(BaseModel):
    id: int
    title: str
    url: Optional[str] = None
    score: int = 0
    by: str
    time: int
    descendants: Optional[int] = 0
    type: str

class HackerNewsResponse(BaseModel):
    total: int
    articles: List[HackerNewsArticle]

class RSSArticle(BaseModel):
    title: str
    link: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    published: Optional[str] = None
    author: Optional[str] = None
    category: Optional[List[str]] = None
    guid: Optional[str] = None

class RSSFeedResponse(BaseModel):
    total: int
    articles: List[RSSArticle]

# Helper functions
async def fetch_hacker_news_article(client: httpx.AsyncClient, story_id: int):
    """Fetch a single Hacker News article"""
    try:
        url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and data.get("type") == "story":
                return HackerNewsArticle(**data)
    except Exception:
        pass
    return None

# API Routes
@app.get("/")
@app.get("/api")
async def root():
    return {"message": "Tech News Hub API", "status": "online"}

@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/hacker-news/", response_model=HackerNewsResponse)
async def get_hacker_news(
    limit: int = Query(10, ge=1, le=100),
    story_type: str = Query("topstories")
):
    """Fetch Hacker News articles"""
    try:
        # Fetch story IDs
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"https://hacker-news.firebaseio.com/v0/{story_type}.json"
            response = await client.get(url)
            story_ids = response.json()[:limit * 2]

            # Fetch articles concurrently
            tasks = [fetch_hacker_news_article(client, sid) for sid in story_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter successful results
            articles = [r for r in results if isinstance(r, HackerNewsArticle)][:limit]

            return HackerNewsResponse(total=len(articles), articles=articles)
    except Exception as e:
        return HackerNewsResponse(total=0, articles=[])

@app.get("/api/v1/rss/", response_model=RSSFeedResponse)
async def get_rss_feed(
    url: str = Query(..., description="RSS feed URL"),
    limit: Optional[int] = Query(20, ge=1, le=100)
):
    """Fetch and parse RSS feed"""
    try:
        # Fetch RSS feed
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url)
            content = response.text

        # Parse feed
        feed = feedparser.parse(content)
        articles = []

        entries = feed.entries[:limit] if limit else feed.entries

        for entry in entries:
            try:
                # Extract categories
                categories = []
                if hasattr(entry, 'tags'):
                    categories = [tag.get('term') for tag in entry.tags if tag.get('term')]

                # Extract author
                author = entry.get('author') or (entry.author_detail.get('name') if hasattr(entry, 'author_detail') else None)

                # Extract published date
                published = entry.get('published') or entry.get('updated')

                # Extract description/content
                description = entry.get('summary') or entry.get('description')
                content = None
                if hasattr(entry, 'content') and entry.content:
                    content = entry.content[0].get('value') if isinstance(entry.content, list) else entry.content

                article = RSSArticle(
                    title=entry.get('title', 'No Title'),
                    link=entry.get('link'),
                    description=description,
                    summary=entry.get('summary'),
                    content=content,
                    published=published,
                    author=author,
                    category=categories if categories else None,
                    guid=entry.get('id') or entry.get('link')
                )
                articles.append(article)
            except Exception:
                continue

        return RSSFeedResponse(total=len(articles), articles=articles)
    except Exception as e:
        return RSSFeedResponse(total=0, articles=[])

# Vercel serverless handler
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except Exception as e:
    print(f"Error creating Mangum handler: {e}")
    # Fallback handler for debugging
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Handler initialization error: {str(e)}"
        }
