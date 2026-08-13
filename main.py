from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from typing import Literal
from datetime import datetime

import models
from database import engine, get_db


app = FastAPI()

# Create database tables if they do not exist
models.Base.metadata.create_all(bind=engine)


# Define the structure of an Issue received from the user
class Issue(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"

    # Prevent empty values or values containing only spaces
    @field_validator("title", "description")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty")

        return value


# Define the structure of an Issue returned by the API
class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "resolved", "closed"]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Root endpoint
@app.get("/")
def home():
    return {"message": "Smart Issue Tracker API"}


# CREATE - Create a new Issue
@app.post("/issues", response_model=IssueResponse)
def create_issue(
    issue: Issue,
    db: Session = Depends(get_db)
):
    new_issue = models.IssueModel(
        title=issue.title,
        description=issue.description,
        priority=issue.priority,
        status=issue.status
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue


# READ - Get all Issues with optional filtering, search and pagination
@app.get("/issues", response_model=list[IssueResponse])
def get_issues(
    status: Literal["open", "in_progress", "resolved", "closed"] | None = None,
    priority: Literal["low", "medium", "high"] | None = None,
    search: str | None = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = select(models.IssueModel)

    if status is not None:
        query = query.where(
            models.IssueModel.status == status
        )

    if priority is not None:
        query = query.where(
            models.IssueModel.priority == priority
        )

    if search is not None:
        query = query.where(
            or_(
                models.IssueModel.title.contains(search),
                models.IssueModel.description.contains(search)
            )
        )

    query = query.offset(offset).limit(limit)

    issues = db.scalars(query).all()

    return issues


# READ - Get one Issue by ID
@app.get("/issues/{issue_id}", response_model=IssueResponse)
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db)
):
    issue = db.get(
        models.IssueModel,
        issue_id
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    return issue


# UPDATE - Update an existing Issue
@app.put("/issues/{issue_id}", response_model=IssueResponse)
def update_issue(
    issue_id: int,
    updated_issue: Issue,
    db: Session = Depends(get_db)
):
    issue = db.get(
        models.IssueModel,
        issue_id
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    issue.title = updated_issue.title
    issue.description = updated_issue.description
    issue.priority = updated_issue.priority
    issue.status = updated_issue.status

    db.commit()
    db.refresh(issue)

    return issue


# DELETE - Delete an Issue by ID
@app.delete("/issues/{issue_id}")
def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db)
):
    issue = db.get(
        models.IssueModel,
        issue_id
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    db.delete(issue)
    db.commit()

    return {"message": "Issue deleted"}