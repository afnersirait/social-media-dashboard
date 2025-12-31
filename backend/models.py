from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)  # twitter, facebook, instagram, linkedin
    account_name = Column(String)
    account_id = Column(String, unique=True)
    access_token = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="account")
    analytics = relationship("Analytics", back_populates="account")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    content = Column(Text)
    media_url = Column(String, nullable=True)
    scheduled_time = Column(DateTime, nullable=True)
    published_time = Column(DateTime, nullable=True)
    status = Column(String, default="draft")  # draft, scheduled, published, failed
    post_type = Column(String, default="text")  # text, image, video, link
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    account = relationship("SocialAccount", back_populates="posts")
    engagement = relationship("Engagement", back_populates="post", uselist=False)


class Engagement(Base):
    __tablename__ = "engagement"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), unique=True)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    post = relationship("Post", back_populates="engagement")


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    date = Column(DateTime, index=True)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    total_posts = Column(Integer, default=0)
    total_engagement = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    profile_views = Column(Integer, default=0)
    
    account = relationship("SocialAccount", back_populates="analytics")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_name = Column(String)
    author_id = Column(String)
    content = Column(Text)
    sentiment = Column(String, nullable=True)  # positive, negative, neutral
    created_at = Column(DateTime, default=datetime.utcnow)
