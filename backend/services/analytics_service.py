from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Dict
import random
from models import Analytics, Post, Engagement, SocialAccount
from redis_client import redis_client


class AnalyticsService:
    @staticmethod
    def get_dashboard_stats(db: Session) -> Dict:
        """Get overall dashboard statistics"""
        cache_key = "dashboard:stats"
        cached = redis_client.get(cache_key)
        
        if cached:
            return cached

        # Get total followers across all accounts
        total_followers = db.query(func.sum(Analytics.followers)).scalar() or 0
        
        # Get total posts
        total_posts = db.query(func.count(Post.id)).filter(
            Post.status == "published"
        ).scalar() or 0
        
        # Get total engagement
        total_engagement = db.query(
            func.sum(Engagement.likes + Engagement.comments + Engagement.shares)
        ).scalar() or 0
        
        # Calculate engagement rate
        engagement_rate = (total_engagement / total_posts * 100) if total_posts > 0 else 0
        
        # Calculate growth rate (last 7 days vs previous 7 days)
        today = datetime.utcnow()
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)
        
        current_week_followers = db.query(func.avg(Analytics.followers)).filter(
            Analytics.date >= week_ago
        ).scalar() or 0
        
        previous_week_followers = db.query(func.avg(Analytics.followers)).filter(
            Analytics.date >= two_weeks_ago,
            Analytics.date < week_ago
        ).scalar() or 1
        
        growth_rate = ((current_week_followers - previous_week_followers) / previous_week_followers * 100) if previous_week_followers > 0 else 0
        
        stats = {
            "total_followers": int(total_followers),
            "total_posts": total_posts,
            "total_engagement": int(total_engagement),
            "engagement_rate": round(engagement_rate, 2),
            "growth_rate": round(growth_rate, 2)
        }
        
        redis_client.set(cache_key, stats, expire=300)  # Cache for 5 minutes
        return stats

    @staticmethod
    def get_engagement_trends(db: Session, days: int = 30) -> List[Dict]:
        """Get engagement trends over time"""
        cache_key = f"engagement:trends:{days}"
        cached = redis_client.get(cache_key)
        
        if cached:
            return cached

        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily engagement data
        results = db.query(
            func.date(Post.published_time).label('date'),
            func.sum(Engagement.likes).label('likes'),
            func.sum(Engagement.comments).label('comments'),
            func.sum(Engagement.shares).label('shares'),
            func.sum(Engagement.views).label('views')
        ).join(
            Engagement, Post.id == Engagement.post_id
        ).filter(
            Post.published_time >= start_date,
            Post.status == "published"
        ).group_by(
            func.date(Post.published_time)
        ).order_by(
            func.date(Post.published_time)
        ).all()
        
        trends = [
            {
                "date": str(result.date) if result.date else "",
                "likes": result.likes or 0,
                "comments": result.comments or 0,
                "shares": result.shares or 0,
                "views": result.views or 0
            }
            for result in results
        ]
        
        redis_client.set(cache_key, trends, expire=600)  # Cache for 10 minutes
        return trends

    @staticmethod
    def get_platform_stats(db: Session) -> List[Dict]:
        """Get statistics by platform"""
        cache_key = "platform:stats"
        cached = redis_client.get(cache_key)
        
        if cached:
            return cached

        accounts = db.query(SocialAccount).filter(SocialAccount.is_active == True).all()
        
        platform_stats = []
        for account in accounts:
            # Get latest analytics
            latest_analytics = db.query(Analytics).filter(
                Analytics.account_id == account.id
            ).order_by(Analytics.date.desc()).first()
            
            # Get post count
            post_count = db.query(func.count(Post.id)).filter(
                Post.account_id == account.id,
                Post.status == "published"
            ).scalar() or 0
            
            # Get total engagement
            total_engagement = db.query(
                func.sum(Engagement.likes + Engagement.comments + Engagement.shares)
            ).join(
                Post, Engagement.post_id == Post.id
            ).filter(
                Post.account_id == account.id
            ).scalar() or 0
            
            platform_stats.append({
                "platform": account.platform,
                "account_name": account.account_name,
                "followers": latest_analytics.followers if latest_analytics else 0,
                "posts": post_count,
                "engagement": int(total_engagement)
            })
        
        redis_client.set(cache_key, platform_stats, expire=600)
        return platform_stats

    @staticmethod
    def get_top_posts(db: Session, limit: int = 10) -> List[Dict]:
        """Get top performing posts"""
        cache_key = f"top:posts:{limit}"
        cached = redis_client.get(cache_key)
        
        if cached:
            return cached

        results = db.query(
            Post,
            Engagement,
            SocialAccount
        ).join(
            Engagement, Post.id == Engagement.post_id
        ).join(
            SocialAccount, Post.account_id == SocialAccount.id
        ).filter(
            Post.status == "published"
        ).order_by(
            (Engagement.likes + Engagement.comments + Engagement.shares).desc()
        ).limit(limit).all()
        
        top_posts = [
            {
                "id": post.id,
                "content": post.content[:100] + "..." if len(post.content) > 100 else post.content,
                "platform": account.platform,
                "published_time": post.published_time.isoformat() if post.published_time else None,
                "likes": engagement.likes,
                "comments": engagement.comments,
                "shares": engagement.shares,
                "total_engagement": engagement.likes + engagement.comments + engagement.shares
            }
            for post, engagement, account in results
        ]
        
        redis_client.set(cache_key, top_posts, expire=600)
        return top_posts

    @staticmethod
    def get_audience_demographics(db: Session, account_id: int = None) -> Dict:
        """Get audience demographics (mock data for demo)"""
        cache_key = f"demographics:{account_id or 'all'}"
        cached = redis_client.get(cache_key)
        
        if cached:
            return cached

        # In a real application, this would come from social media APIs
        demographics = {
            "age_groups": [
                {"range": "18-24", "percentage": 25},
                {"range": "25-34", "percentage": 35},
                {"range": "35-44", "percentage": 20},
                {"range": "45-54", "percentage": 12},
                {"range": "55+", "percentage": 8}
            ],
            "gender": [
                {"type": "Male", "percentage": 52},
                {"type": "Female", "percentage": 45},
                {"type": "Other", "percentage": 3}
            ],
            "locations": [
                {"country": "United States", "percentage": 40},
                {"country": "United Kingdom", "percentage": 15},
                {"country": "Canada", "percentage": 12},
                {"country": "Australia", "percentage": 10},
                {"country": "Others", "percentage": 23}
            ]
        }
        
        redis_client.set(cache_key, demographics, expire=3600)
        return demographics
