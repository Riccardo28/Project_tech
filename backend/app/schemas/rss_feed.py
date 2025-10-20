from pydantic import BaseModel, Field
from typing import Optional, List


class RSSArticle(BaseModel):
    """Schema for generic RSS feed article"""
    title: str = Field(..., description="Article title")
    link: Optional[str] = Field(None, description="Article URL")
    description: Optional[str] = Field(None, description="Article description/summary")
    published: Optional[str] = Field(None, description="Publication date")
    author: Optional[str] = Field(None, description="Article author")
    category: Optional[List[str]] = Field(None, description="Article categories/tags")
    guid: Optional[str] = Field(None, description="Unique identifier for the article")


class RSSFeedInfo(BaseModel):
    """Schema for RSS feed metadata"""
    title: Optional[str] = Field(None, description="Feed title")
    link: Optional[str] = Field(None, description="Feed URL")
    description: Optional[str] = Field(None, description="Feed description")
    language: Optional[str] = Field(None, description="Feed language")


class RSSFeedResponse(BaseModel):
    """Response schema for RSS feed articles"""
    feed_info: RSSFeedInfo = Field(..., description="RSS feed metadata")
    total: int = Field(..., description="Total number of articles fetched")
    articles: List[RSSArticle] = Field(..., description="List of articles")
