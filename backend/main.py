from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import analytics, posts, accounts
import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Social Media Dashboard API",
    description="API for social media analytics and management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analytics.router)
app.include_router(posts.router)
app.include_router(accounts.router)


@app.get("/")
def root():
    return {
        "message": "Social Media Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Seed data endpoint for demo purposes
@app.post("/api/seed")
def seed_data():
    """Seed the database with sample data for demo purposes"""
    from sqlalchemy.orm import Session
    from database import SessionLocal
    from datetime import datetime, timedelta
    import random
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_accounts = db.query(models.SocialAccount).count()
        if existing_accounts > 0:
            return {"message": "Database already seeded"}
        
        # Create social accounts
        platforms = [
            {"platform": "twitter", "name": "TechStartup", "id": "techstartup_tw"},
            {"platform": "facebook", "name": "TechStartup", "id": "techstartup_fb"},
            {"platform": "instagram", "name": "techstartup", "id": "techstartup_ig"},
            {"platform": "linkedin", "name": "TechStartup Inc", "id": "techstartup_li"}
        ]
        
        accounts = []
        for p in platforms:
            account = models.SocialAccount(
                platform=p["platform"],
                account_name=p["name"],
                account_id=p["id"],
                is_active=True
            )
            db.add(account)
            accounts.append(account)
        
        db.commit()
        
        # Create analytics data for the past 30 days
        for account in accounts:
            base_followers = random.randint(5000, 50000)
            for i in range(30):
                date = datetime.utcnow() - timedelta(days=29-i)
                analytics = models.Analytics(
                    account_id=account.id,
                    date=date,
                    followers=base_followers + (i * random.randint(50, 200)),
                    following=random.randint(100, 500),
                    total_posts=random.randint(50, 200),
                    total_engagement=random.randint(1000, 5000),
                    reach=random.randint(10000, 100000),
                    impressions=random.randint(20000, 200000),
                    profile_views=random.randint(500, 5000)
                )
                db.add(analytics)
        
        db.commit()
        
        # Create posts
        post_contents = [
            "Excited to announce our new product launch! 🚀",
            "Check out our latest blog post on industry trends",
            "Join us for our upcoming webinar next week!",
            "Customer success story: How we helped increase ROI by 300%",
            "Behind the scenes at our office today 📸",
            "New feature alert! Now you can do even more with our platform",
            "Thank you for 10K followers! Here's to many more milestones 🎉",
            "Quick tip: Here's how to maximize your productivity",
            "We're hiring! Check out our open positions",
            "Happy Friday! What are your weekend plans?"
        ]
        
        for account in accounts:
            for i in range(15):
                days_ago = random.randint(0, 29)
                published_time = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
                
                post = models.Post(
                    account_id=account.id,
                    content=random.choice(post_contents),
                    status="published",
                    post_type=random.choice(["text", "image", "video"]),
                    published_time=published_time,
                    created_at=published_time - timedelta(hours=1)
                )
                db.add(post)
                db.flush()
                
                # Create engagement for the post
                engagement = models.Engagement(
                    post_id=post.id,
                    likes=random.randint(50, 1000),
                    comments=random.randint(5, 100),
                    shares=random.randint(10, 200),
                    views=random.randint(500, 10000),
                    clicks=random.randint(20, 500)
                )
                engagement.engagement_rate = (
                    (engagement.likes + engagement.comments + engagement.shares + engagement.clicks) 
                    / engagement.views * 100
                ) if engagement.views > 0 else 0
                db.add(engagement)
        
        # Create some scheduled posts
        for account in accounts[:2]:
            for i in range(3):
                scheduled_time = datetime.utcnow() + timedelta(days=i+1, hours=random.randint(9, 17))
                post = models.Post(
                    account_id=account.id,
                    content=f"Scheduled post for {scheduled_time.strftime('%B %d')}",
                    status="scheduled",
                    post_type="text",
                    scheduled_time=scheduled_time
                )
                db.add(post)
        
        db.commit()
        
        return {
            "message": "Database seeded successfully",
            "accounts": len(accounts),
            "posts": db.query(models.Post).count()
        }
        
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
