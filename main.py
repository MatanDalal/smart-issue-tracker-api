from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Issue(BaseModel):
    title: str
    description: str
    priority: str

issues = []

@app.get("/")
def home():
    return {"message": "Smart Issue Tracker API"}

@app.post("/issues")
def create_issue(issue: Issue):
    new_issue = {
        "id": len(issues) + 1,
        "title": issue.title,
        "description": issue.description,
        "priority": issue.priority
    }

    issues.append(new_issue)
    return new_issue

@app.get("/issues")
def get_issues():
    return issues

@app.get("/issues/{issue_id}")
def get_issue(issue_id: int):
    for issue in issues:
        if issue["id"] == issue_id:
            return issue

    raise HTTPException(status_code=404, detail="Issue not found")

@app.delete("/issues/{issue_id}")
def delete_issue(issue_id: int):
    for issue in issues:
        if issue["id"] == issue_id:
            issues.remove(issue)
            return {"message": "Issue deleted"}

    raise HTTPException(status_code=404, detail="Issue not found")

@app.put("/issues/{issue_id}")
def update_issue(issue_id: int, updated_issue: Issue):
    for issue in issues:
        if issue["id"] == issue_id:
            issue["title"] = updated_issue.title
            issue["description"] = updated_issue.description
            issue["priority"] = updated_issue.priority
            return issue

    raise HTTPException(status_code=404, detail="Issue not found")