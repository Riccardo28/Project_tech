from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from app.schemas.rss_feed import RSSFeedResponse, RSSArticle
from app.services.rss_feed import RSSFeedService

router = APIRouter()


@router.get("/", response_model=RSSFeedResponse)
async def fetch_rss_feed(
    url: str = Query(..., description="RSS feed URL to fetch"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Maximum number of articles to fetch")
):
    """
    Fetch articles from any RSS feed URL

    - **url**: RSS feed URL (e.g., https://www.techradar.com/rss)
    - **limit**: Optional limit on number of articles (default: all articles)

    Example URLs:
    - TechRadar: https://www.techradar.com/rss
    - BBC News: http://feeds.bbci.co.uk/news/rss.xml
    - Hacker News: https://news.ycombinator.com/rss
    """
    try:
        response = await RSSFeedService.fetch_feed(url, limit)
        return response
    except Exception as e:
        import traceback
        print(f"Error fetching RSS feed from {url}: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching RSS feed: {str(e)}"
        )


@router.post("/multiple", response_model=dict)
async def fetch_multiple_rss_feeds(
    urls: List[str] = Query(..., description="List of RSS feed URLs"),
    limit_per_feed: Optional[int] = Query(5, ge=1, le=50, description="Maximum articles per feed")
):
    """
    Fetch articles from multiple RSS feeds at once

    - **urls**: List of RSS feed URLs
    - **limit_per_feed**: Maximum number of articles to fetch per feed

    Returns combined articles from all feeds
    """
    try:
        articles = await RSSFeedService.fetch_multiple_feeds(urls, limit_per_feed)
        return {
            "total_feeds": len(urls),
            "total_articles": len(articles),
            "articles": articles
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching multiple RSS feeds: {str(e)}"
        )


@router.get("/techradar", response_model=RSSFeedResponse)
async def fetch_techradar_rss(
    limit: Optional[int] = Query(10, ge=1, le=100, description="Maximum number of articles to fetch")
):
    """
    Quick endpoint to fetch TechRadar RSS feed

    - **limit**: Maximum number of articles to fetch (default: 10)
    """
    try:
        techradar_url = "https://www.techradar.com/rss"
        response = await RSSFeedService.fetch_feed(techradar_url, limit)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching TechRadar RSS feed: {str(e)}"
        )
