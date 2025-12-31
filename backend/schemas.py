from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class SocialAccountBase(BaseModel):
    platform: str
    account_name: str
    account_id: str


class SocialAccountCreate(SocialAccountBase):
    access_token: Optional[str] = None


class SocialAccount(SocialAccountBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    content: str
    media_url: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    post_type: str = "text"


class PostCreate(PostBase):
    account_id: int


class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    status: Optional[str] = None


class EngagementData(BaseModel):
    likes: int = 0
    comments: int = 0
    shares: int = 0
    views: int = 0
    clicks: int = 0
    engagement_rate: float = 0.0


class Post(PostBase):
    id: int
    account_id: int
    status: str
    published_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    engagement: Optional[EngagementData] = None

    class Config:
        from_attributes = True


class AnalyticsBase(BaseModel):
    date: datetime
    followers: int = 0
    following: int = 0
    total_posts: int = 0
    total_engagement: int = 0
    reach: int = 0
    impressions: int = 0
    profile_views: int = 0


class AnalyticsCreate(AnalyticsBase):
    account_id: int


class Analytics(AnalyticsBase):
    id: int
    account_id: int

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    author_name: str
    author_id: str
    content: str
    sentiment: Optional[str] = None


class CommentCreate(CommentBase):
    post_id: int


class Comment(CommentBase):
    id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_followers: int
    total_posts: int
    total_engagement: int
    engagement_rate: float
    growth_rate: float


class EngagementTrend(BaseModel):
    date: str
    likes: int
    comments: int
    shares: int
    views: int


class PlatformStats(BaseModel):
    platform: str
    followers: int
    posts: int
    engagement: int
