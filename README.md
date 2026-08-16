# Smart Issue Tracker API

A RESTful Issue Tracking API built with FastAPI, SQLAlchemy, Pydantic, and SQLite.

The application allows users to create, view, update, delete, search, filter, and paginate software issues through a structured API.

## Live Demo

- Live API: https://smart-issue-tracker-api.onrender.com
- Swagger API Documentation: https://smart-issue-tracker-api.onrender.com/docs

## Features

- Create new issues
- View all issues
- View a specific issue by ID
- Update existing issues
- Delete issues
- Filter issues by status
- Filter issues by priority
- Search issues by title or description
- Pagination using limit and offset
- Input validation
- Automatic creation and update timestamps
- Structured API response models
- Automatic interactive API documentation with Swagger UI
- Public deployment on Render

## Issue Fields

Each issue contains:

- `id` - Unique issue identifier
- `title` - Issue title
- `description` - Detailed issue description
- `priority` - `low`, `medium`, or `high`
- `status` - `open`, `in_progress`, `resolved`, or `closed`
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn
- Render
- Git / GitHub

## Project Structure

```text
smart-issue-tracker-api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── .gitignore
└── README.md
```

### File Responsibilities

- `main.py` - API endpoints and application logic
- `database.py` - Database connection and session management
- `models.py` - SQLAlchemy database models
- `schemas.py` - Pydantic request/response schemas and validation
- `requirements.txt` - Python dependencies

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | API health/root endpoint |
| POST | `/issues` | Create a new issue |
| GET | `/issues` | Get issues with optional filters, search, and pagination |
| GET | `/issues/{issue_id}` | Get a specific issue |
| PUT | `/issues/{issue_id}` | Update an issue |
| DELETE | `/issues/{issue_id}` | Delete an issue |

## Filtering

Issues can be filtered by status:

```text
GET /issues?status=open
```

Or by priority:

```text
GET /issues?priority=high
```

Filters can also be combined:

```text
GET /issues?status=in_progress&priority=high
```

## Search

Search is supported across issue titles and descriptions:

```text
GET /issues?search=database
```

Search can also be combined with filters.

## Pagination

The API supports pagination using `limit` and `offset`.

Example:

```text
GET /issues?limit=10&offset=0
```

- `limit` - Number of issues to return (1-100)
- `offset` - Number of issues to skip

## Validation

The API validates incoming data before storing it.

Examples of validation rules:

- Title cannot be empty
- Description cannot be empty
- Title maximum length is 100 characters
- Description maximum length is 1000 characters
- Priority must be `low`, `medium`, or `high`
- Status must be `open`, `in_progress`, `resolved`, or `closed`
- Pagination values must be within valid ranges

## Installation

Clone the repository:

```bash
git clone https://github.com/MatanDalal/smart-issue-tracker-api.git
```

Move into the project directory:

```bash
cd smart-issue-tracker-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The local API will be available at:

```text
http://127.0.0.1:8000
```

Local Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Example Issue

```json
{
  "title": "Login button not working",
  "description": "Users cannot submit the login form.",
  "priority": "high",
  "status": "open"
}
```

## Error Handling

The API includes validation and error handling for cases such as:

- Invalid priority or status values
- Invalid pagination parameters
- Empty issue titles or descriptions
- Requests for issues that do not exist

For example, requesting an unknown issue returns:

```json
{
  "detail": "Issue not found"
}
```

## Future Development

Planned improvements include:

- Frontend user interface
- Authentication and users
- Issue assignment
- Additional sorting options
- Migration from SQLite to a production database such as PostgreSQL

## Author

Matan Dalal