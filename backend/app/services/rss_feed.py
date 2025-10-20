import feedparser
import httpx
from typing import List, Optional
from app.schemas.rss_feed import RSSArticle, RSSFeedInfo, RSSFeedResponse


class RSSFeedService:
    """Service for fetching and parsing RSS feeds from any source"""

    TIMEOUT = 30.0

    @staticmethod
    async def fetch_feed(url: str, limit: Optional[int] = None) -> RSSFeedResponse:
        """
        Fetch and parse an RSS feed from any URL

        Args:
            url: RSS feed URL
            limit: Maximum number of articles to return (None for all)

        Returns:
            RSSFeedResponse with feed info and articles
        """
        try:
            # Fetch the RSS feed content
            async with httpx.AsyncClient(timeout=RSSFeedService.TIMEOUT, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
                content = response.text

            # Parse the RSS feed
            feed = feedparser.parse(content)

            # Extract feed metadata
            feed_info = RSSFeedInfo(
                title=feed.feed.get('title'),
                link=feed.feed.get('link'),
                description=feed.feed.get('description') or feed.feed.get('subtitle'),
                language=feed.feed.get('language')
            )

            # Extract articles
            articles = []
            entries = feed.entries[:limit] if limit else feed.entries

            for entry in entries:
                try:
                    # Extract categories/tags
                    categories = []
                    if hasattr(entry, 'tags'):
                        categories = [tag.get('term') for tag in entry.tags if tag.get('term')]
                    elif hasattr(entry, 'category'):
                        categories = [entry.category]

                    # Extract author
                    author = None
                    if hasattr(entry, 'author'):
                        author = entry.author
                    elif hasattr(entry, 'author_detail'):
                        author = entry.author_detail.get('name')

                    # Extract publication date
                    published = None
                    if hasattr(entry, 'published'):
                        published = entry.published
                    elif hasattr(entry, 'updated'):
                        published = entry.updated

                    # Extract description/content
                    description = None
                    if hasattr(entry, 'summary'):
                        description = entry.summary
                    elif hasattr(entry, 'description'):
                        description = entry.description
                    elif hasattr(entry, 'content') and entry.content:
                        # Some feeds use 'content' instead of 'summary'
                        description = entry.content[0].get('value') if isinstance(entry.content, list) else entry.content

                    # Create article object
                    article = RSSArticle(
                        title=entry.get('title', 'No Title'),
                        link=entry.get('link'),
                        description=description,
                        published=published,
                        author=author,
                        category=categories if categories else None,
                        guid=entry.get('id') or entry.get('link')
                    )
                    articles.append(article)
                except Exception as article_error:
                    # Log the error but continue processing other articles
                    print(f"Error processing article from {url}: {str(article_error)}")
                    continue

            return RSSFeedResponse(
                feed_info=feed_info,
                total=len(articles),
                articles=articles
            )

        except httpx.HTTPError as e:
            raise Exception(f"HTTP error fetching RSS feed: {str(e)}")
        except Exception as e:
            raise Exception(f"Error parsing RSS feed: {str(e)}")

    @staticmethod
    async def fetch_multiple_feeds(urls: List[str], limit_per_feed: Optional[int] = None) -> List[RSSArticle]:
        """
        Fetch articles from multiple RSS feeds

        Args:
            urls: List of RSS feed URLs
            limit_per_feed: Maximum number of articles per feed

        Returns:
            Combined list of articles from all feeds
        """
        all_articles = []

        for url in urls:
            try:
                response = await RSSFeedService.fetch_feed(url, limit_per_feed)
                # Add source info to each article
                for article in response.articles:
                    all_articles.append(article)
            except Exception as e:
                print(f"Error fetching feed {url}: {str(e)}")
                continue

        return all_articles
