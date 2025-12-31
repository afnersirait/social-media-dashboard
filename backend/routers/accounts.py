from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import SocialAccount, Analytics
from schemas import SocialAccount as SocialAccountSchema, SocialAccountCreate, Analytics as AnalyticsSchema, AnalyticsCreate
from datetime import datetime

router = APIRouter(prefix="/api/accounts", tags=["accounts"])


@router.post("/", response_model=SocialAccountSchema)
def create_account(account: SocialAccountCreate, db: Session = Depends(get_db)):
    """Create a new social media account"""
    # Check if account already exists
    existing = db.query(SocialAccount).filter(
        SocialAccount.account_id == account.account_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Account already exists")
    
    db_account = SocialAccount(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("/", response_model=List[SocialAccountSchema])
def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all social media accounts"""
    accounts = db.query(SocialAccount).filter(
        SocialAccount.is_active == True
    ).offset(skip).limit(limit).all()
    return accounts


@router.get("/{account_id}", response_model=SocialAccountSchema)
def get_account(account_id: int, db: Session = Depends(get_db)):
    """Get a specific account"""
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """Deactivate an account"""
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account.is_active = False
    db.commit()
    return {"message": "Account deactivated successfully"}


@router.post("/{account_id}/analytics", response_model=AnalyticsSchema)
def add_analytics(account_id: int, analytics: AnalyticsCreate, db: Session = Depends(get_db)):
    """Add analytics data for an account"""
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db_analytics = Analytics(**analytics.model_dump())
    db.add(db_analytics)
    db.commit()
    db.refresh(db_analytics)
    return db_analytics


@router.get("/{account_id}/analytics", response_model=List[AnalyticsSchema])
def get_account_analytics(
    account_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get analytics history for an account"""
    from datetime import timedelta
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    analytics = db.query(Analytics).filter(
        Analytics.account_id == account_id,
        Analytics.date >= start_date
    ).order_by(Analytics.date.desc()).all()
    
    return analytics
