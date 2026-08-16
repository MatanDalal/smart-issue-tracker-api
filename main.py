from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from schemas import Issue, IssueResponse, Priority, IssueStatus

app = FastAPI()

# Create database tables if they do not exist
models.Base.metadata.create_all(bind=engine)

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
    status: IssueStatus | None = None,
    priority: Priority | None = None,
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