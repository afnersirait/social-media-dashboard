from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from services.post_service import PostService
from schemas import Post, PostCreate, PostUpdate

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post("/", response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Create a new post"""
    try:
        return PostService.create_post(db, post)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[Post])
def get_posts(
    account_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get posts with optional filters"""
    return PostService.get_posts(db, account_id, status, skip, limit)


@router.get("/scheduled", response_model=List[Post])
def get_scheduled_posts(db: Session = Depends(get_db)):
    """Get all scheduled posts"""
    return PostService.get_scheduled_posts(db)


@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a single post by ID"""
    post = PostService.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=Post)
def update_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    """Update a post"""
    post = PostService.update_post(db, post_id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    success = PostService.delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}


@router.post("/{post_id}/publish", response_model=Post)
def publish_post(post_id: int, db: Session = Depends(get_db)):
    """Publish a post"""
    post = PostService.publish_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}/engagement")
def update_engagement(
    post_id: int,
    likes: int = 0,
    comments: int = 0,
    shares: int = 0,
    views: int = 0,
    clicks: int = 0,
    db: Session = Depends(get_db)
):
    """Update engagement metrics for a post"""
    engagement = PostService.update_engagement(
        db, post_id, likes, comments, shares, views, clicks
    )
    if not engagement:
        raise HTTPException(status_code=404, detail="Post not found")
    return engagement
