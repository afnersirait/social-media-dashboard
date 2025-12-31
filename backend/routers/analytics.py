from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.analytics_service import AnalyticsService
from schemas import DashboardStats, EngagementTrend, PlatformStats

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get overall dashboard statistics"""
    return AnalyticsService.get_dashboard_stats(db)


@router.get("/trends", response_model=List[EngagementTrend])
def get_engagement_trends(days: int = 30, db: Session = Depends(get_db)):
    """Get engagement trends over specified days"""
    if days < 1 or days > 365:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
    return AnalyticsService.get_engagement_trends(db, days)


@router.get("/platforms", response_model=List[PlatformStats])
def get_platform_stats(db: Session = Depends(get_db)):
    """Get statistics by platform"""
    return AnalyticsService.get_platform_stats(db)


@router.get("/top-posts")
def get_top_posts(limit: int = 10, db: Session = Depends(get_db)):
    """Get top performing posts"""
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    return AnalyticsService.get_top_posts(db, limit)


@router.get("/demographics")
def get_audience_demographics(account_id: int = None, db: Session = Depends(get_db)):
    """Get audience demographics"""
    return AnalyticsService.get_audience_demographics(db, account_id)
