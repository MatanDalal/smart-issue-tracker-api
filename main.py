from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import engine, get_db


app = FastAPI()

# Create database tables if they do not exist
models.Base.metadata.create_all(bind=engine)


# Define the structure of an Issue received from the user
class Issue(BaseModel):
    title: str
    description: str
    priority: str


# Root endpoint
@app.get("/")
def home():
    return {"message": "Smart Issue Tracker API"}


# CREATE - Create a new Issue
@app.post("/issues")
def create_issue(issue: Issue, db: Session = Depends(get_db)):

    new_issue = models.IssueModel(
        title=issue.title,
        description=issue.description,
        priority=issue.priority
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue


# READ - Get all Issues
@app.get("/issues")
def get_issues(db: Session = Depends(get_db)):

    issues = db.scalars(
        select(models.IssueModel)
    ).all()

    return issues


# READ - Get one Issue by ID
@app.get("/issues/{issue_id}")
def get_issue(issue_id: int, db: Session = Depends(get_db)):

    issue = db.get(models.IssueModel, issue_id)

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    return issue


# DELETE - Delete an Issue by ID
@app.delete("/issues/{issue_id}")
def delete_issue(issue_id: int, db: Session = Depends(get_db)):

    issue = db.get(models.IssueModel, issue_id)

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    db.delete(issue)
    db.commit()

    return {"message": "Issue deleted"}


# UPDATE - Update an existing Issue
@app.put("/issues/{issue_id}")
def update_issue(
    issue_id: int,
    updated_issue: Issue,
    db: Session = Depends(get_db)
):

    issue = db.get(models.IssueModel, issue_id)

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    issue.title = updated_issue.title
    issue.description = updated_issue.description
    issue.priority = updated_issue.priority

    db.commit()
    db.refresh(issue)

    return issue