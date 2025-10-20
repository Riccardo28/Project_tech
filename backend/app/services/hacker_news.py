import httpx
import asyncio
from typing import List, Optional
from app.schemas.hacker_news import HackerNewsArticle


class HackerNewsService:
    """Service for fetching articles from Hacker News API"""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    TIMEOUT = 10.0

    @staticmethod
    async def fetch_story_ids(story_type: str = "topstories") -> List[int]:
        """
        Fetch story IDs from Hacker News API

        Args:
            story_type: Type of stories (topstories, newstories, beststories, askstories, showstories, jobstories)

        Returns:
            List of story IDs
        """
        url = f"{HackerNewsService.BASE_URL}/{story_type}.json"

        async with httpx.AsyncClient(timeout=HackerNewsService.TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def fetch_article(article_id: int) -> Optional[HackerNewsArticle]:
        """
        Fetch a single article by ID

        Args:
            article_id: Hacker News item ID

        Returns:
            HackerNewsArticle or None if fetch fails
        """
        url = f"{HackerNewsService.BASE_URL}/item/{article_id}.json"

        try:
            async with httpx.AsyncClient(timeout=HackerNewsService.TIMEOUT) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                # Only return if it's a story type
                if data and data.get("type") == "story":
                    return HackerNewsArticle(**data)
                return None
        except Exception as e:
            print(f"Error fetching article {article_id}: {e}")
            return None

    @staticmethod
    async def fetch_articles(
        limit: int = 10,
        story_type: str = "topstories",
        min_score: Optional[int] = None
    ) -> List[HackerNewsArticle]:
        """
        Fetch multiple articles from Hacker News

        Args:
            limit: Number of articles to fetch
            story_type: Type of stories to fetch
            min_score: Minimum score filter (optional)

        Returns:
            List of HackerNewsArticle objects
        """
        # Fetch story IDs
        story_ids = await HackerNewsService.fetch_story_ids(story_type)

        # Limit the number of IDs to fetch
        story_ids = story_ids[:limit * 2]  # Fetch extra in case some fail or don't meet criteria

        # Fetch articles concurrently
        articles = []
        async with httpx.AsyncClient(timeout=HackerNewsService.TIMEOUT) as client:
            async def fetch_single_article(story_id: int):
                """Helper function to fetch a single article"""
                try:
                    url = f"{HackerNewsService.BASE_URL}/item/{story_id}.json"
                    response = await client.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        if data and data.get("type") == "story":
                            return HackerNewsArticle(**data)
                except Exception:
                    pass
                return None

            # Create tasks for concurrent fetching
            tasks = [fetch_single_article(story_id) for story_id in story_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter and collect successful results
            for result in results:
                if isinstance(result, HackerNewsArticle):
                    # Apply min_score filter if provided
                    if min_score is None or result.score >= min_score:
                        articles.append(result)

                        # Stop if we have enough articles
                        if len(articles) >= limit:
                            break

        return articles[:limit]
