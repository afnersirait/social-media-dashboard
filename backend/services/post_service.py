from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from models import Post, Engagement, SocialAccount
from schemas import PostCreate, PostUpdate
from redis_client import redis_client


class PostService:
    @staticmethod
    def create_post(db: Session, post_data: PostCreate) -> Post:
        """Create a new post"""
        # Verify account exists
        account = db.query(SocialAccount).filter(
            SocialAccount.id == post_data.account_id
        ).first()
        
        if not account:
            raise ValueError("Account not found")
        
        # Determine status
        status = "scheduled" if post_data.scheduled_time else "draft"
        
        post = Post(
            account_id=post_data.account_id,
            content=post_data.content,
            media_url=post_data.media_url,
            scheduled_time=post_data.scheduled_time,
            post_type=post_data.post_type,
            status=status
        )
        
        db.add(post)
        db.commit()
        db.refresh(post)
        
        # Create engagement record
        engagement = Engagement(post_id=post.id)
        db.add(engagement)
        db.commit()
        
        # Invalidate cache
        redis_client.delete("posts:all")
        redis_client.delete(f"posts:account:{post_data.account_id}")
        
        return post

    @staticmethod
    def get_posts(
        db: Session,
        account_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:
        """Get posts with optional filters"""
        query = db.query(Post)
        
        if account_id:
            query = query.filter(Post.account_id == account_id)
        
        if status:
            query = query.filter(Post.status == status)
        
        posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
        return posts

    @staticmethod
    def get_post(db: Session, post_id: int) -> Optional[Post]:
        """Get a single post by ID"""
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def update_post(db: Session, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        """Update a post"""
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            return None
        
        update_data = post_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(post, key, value)
        
        post.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(post)
        
        # Invalidate cache
        redis_client.delete("posts:all")
        redis_client.delete(f"posts:account:{post.account_id}")
        redis_client.delete(f"post:{post_id}")
        
        return post

    @staticmethod
    def delete_post(db: Session, post_id: int) -> bool:
        """Delete a post"""
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            return False
        
        # Delete associated engagement
        db.query(Engagement).filter(Engagement.post_id == post_id).delete()
        
        db.delete(post)
        db.commit()
        
        # Invalidate cache
        redis_client.delete("posts:all")
        redis_client.delete(f"posts:account:{post.account_id}")
        redis_client.delete(f"post:{post_id}")
        
        return True

    @staticmethod
    def publish_post(db: Session, post_id: int) -> Optional[Post]:
        """Publish a post"""
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            return None
        
        post.status = "published"
        post.published_time = datetime.utcnow()
        post.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(post)
        
        # Invalidate cache
        redis_client.delete("posts:all")
        redis_client.delete(f"posts:account:{post.account_id}")
        redis_client.delete("dashboard:stats")
        
        return post

    @staticmethod
    def get_scheduled_posts(db: Session) -> List[Post]:
        """Get all scheduled posts"""
        return db.query(Post).filter(
            Post.status == "scheduled",
            Post.scheduled_time.isnot(None)
        ).order_by(Post.scheduled_time).all()

    @staticmethod
    def update_engagement(
        db: Session,
        post_id: int,
        likes: int = 0,
        comments: int = 0,
        shares: int = 0,
        views: int = 0,
        clicks: int = 0
    ) -> Optional[Engagement]:
        """Update engagement metrics for a post"""
        engagement = db.query(Engagement).filter(
            Engagement.post_id == post_id
        ).first()
        
        if not engagement:
            return None
        
        engagement.likes = likes
        engagement.comments = comments
        engagement.shares = shares
        engagement.views = views
        engagement.clicks = clicks
        
        # Calculate engagement rate
        if views > 0:
            total_engagement = likes + comments + shares + clicks
            engagement.engagement_rate = (total_engagement / views) * 100
        
        engagement.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(engagement)
        
        # Invalidate cache
        redis_client.delete("dashboard:stats")
        redis_client.delete(f"engagement:trends:30")
        redis_client.delete(f"post:{post_id}")
        
        return engagement
