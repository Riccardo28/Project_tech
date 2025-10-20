from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from app.schemas.hacker_news import HackerNewsResponse, HackerNewsArticle
from app.services.hacker_news import HackerNewsService

router = APIRouter()


@router.get("/", response_model=HackerNewsResponse)
async def get_hacker_news_articles(
    limit: int = Query(10, ge=1, le=100, description="Number of articles to fetch"),
    story_type: str = Query(
        "topstories",
        description="Type of stories (topstories, newstories, beststories, askstories, showstories, jobstories)"
    ),
    min_score: Optional[int] = Query(None, ge=0, description="Minimum score filter")
):
    """
    Fetch articles from Hacker News API

    - **limit**: Number of articles to fetch (1-100)
    - **story_type**: Type of stories to fetch
    - **min_score**: Optional minimum score filter
    """
    try:
        articles = await HackerNewsService.fetch_articles(
            limit=limit,
            story_type=story_type,
            min_score=min_score
        )

        return HackerNewsResponse(
            total=len(articles),
            articles=articles
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching Hacker News articles: {str(e)}"
        )


@router.get("/{article_id}", response_model=HackerNewsArticle)
async def get_hacker_news_article(article_id: int):
    """
    Fetch a specific article from Hacker News by ID

    - **article_id**: Hacker News item ID
    """
    try:
        article = await HackerNewsService.fetch_article(article_id)

        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with ID {article_id} not found or is not a story"
            )

        return article
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching article: {str(e)}"
        )


@router.get("/top/{limit}", response_model=HackerNewsResponse)
async def get_top_stories(limit: int = 10):
    """
    Quick endpoint to fetch top stories

    - **limit**: Number of top stories to fetch
    """
    try:
        articles = await HackerNewsService.fetch_articles(
            limit=min(limit, 100),
            story_type="topstories"
        )

        return HackerNewsResponse(
            total=len(articles),
            articles=articles
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching top stories: {str(e)}"
        )
