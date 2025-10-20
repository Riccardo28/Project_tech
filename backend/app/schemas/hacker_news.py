from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime


class HackerNewsArticle(BaseModel):
    """Schema for Hacker News article"""
    id: int = Field(..., description="Hacker News item ID")
    title: str = Field(..., description="Article title")
    url: Optional[HttpUrl] = Field(None, description="Article URL")
    score: int = Field(..., description="Article score/points")
    by: str = Field(..., description="Author username")
    time: int = Field(..., description="Unix timestamp")
    descendants: Optional[int] = Field(None, description="Number of comments")
    type: str = Field(..., description="Item type (story, comment, etc.)")

    @property
    def formatted_time(self) -> str:
        """Convert Unix timestamp to readable datetime"""
        return datetime.fromtimestamp(self.time).strftime('%Y-%m-%d %H:%M:%S')


class HackerNewsResponse(BaseModel):
    """Response schema for Hacker News articles"""
    total: int = Field(..., description="Total number of articles fetched")
    articles: List[HackerNewsArticle] = Field(..., description="List of articles")


class HackerNewsFilter(BaseModel):
    """Query parameters for filtering Hacker News articles"""
    min_score: Optional[int] = Field(None, ge=0, description="Minimum score filter")
    limit: int = Field(10, ge=1, le=100, description="Number of articles to fetch")
    story_type: str = Field("topstories", description="Type of stories (topstories, newstories, beststories)")
