# Sprint Manager Backend - AI Coding Agent Instructions

## Architecture Overview

**Stack**: FastAPI (Python 3.11+) + PostgreSQL + SQLAlchemy ORM  
**Database**: PostgreSQL (`localhost:5432/Sprint_Manager`) with hardcoded credentials in `database.py`

### Core Components

- **`main.py`**: FastAPI app initialization with CORS middleware (allows `http://localhost:3000`)
- **`database.py`**: SQLAlchemy session management + `db_dependency` for route injection
- **`models/`**: ORM models (User, Project, Sprint, Task) inheriting from `Base = declarative_base()`
- **`apis/`**: FastAPI routers organized by entity type (users, projects, sprints, tasks)
- **`apis/schemas/`**: Pydantic BaseModel schemas for request/response validation

### Database Schema Relationships

- **User-Project**: Many-to-many via `user_projects` association table (defined in `Project` model)
- **Task-Project**: Foreign key `task.project_id`
- **Task-Sprint**: Foreign key `task.sprint_id`
- **Task-User**: Foreign key `task.user_id` (assignee)
- **Task-Task**: Self-referential via `task.sub_task` (parent-child tasks)
- **Sprint-Project**: Foreign key `sprint.project_id`

## Key Patterns & Conventions

### API Route Structure

All routers follow CRUD pattern:
```python
@router.post("/")  # Create
@router.get("/{id}")  # Get by ID
@router.get("/")  # Get all
@router.put("/{id}")  # Update
```

Routes use dependency injection: `db: Session = Depends(get_db)` from `database.py`

### Pydantic Schemas

- **`Create` schemas**: Input models with validators (see `UserCreate` with email/mobile validation)
- **`Update` schemas**: Mostly optional fields to support partial updates
- **`Get` schemas**: Minimal models for authentication (e.g., `UserGet` with email/password only)
- **Enum fields**: WorkType, Workflow, Priority use `str, Enum` in schemas and PostgreSQL ENUMs in models

### Model Auto-Increment Patterns

- **Task**: Custom code generation (auto-increments from last task code, starts at 1001)
- **Other entities**: Standard SQLAlchemy `primary_key=True` auto-increment

### Database Dependencies

`db_dependency = Annotated[Session, Depends(get_db)]` is defined in `database.py` but routes use inline `Depends(get_db)`—either approach works.

## Critical Developer Workflows

### Development Server
```powershell
uvicorn main:app --reload
```
Runs on `http://localhost:8000` (API docs at `/docs`)

### Database Setup

1. Ensure PostgreSQL running on `localhost:5432`
2. Create database: `CREATE DATABASE Sprint_Manager;`
3. SQLAlchemy auto-creates tables on first FastAPI startup via `Base.metadata.create_all(bind=engine)`

### Environment Variables

- `GEMINI_API_KEY`: Required for AI task processing (`apis/ai.py`), but endpoint not yet configured

## Project-Specific Quirks & Gotchas

### Known Issues

1. **User model incomplete**: `models/user.py` references `user_projects` relationship before it's defined (defined later in `Project` model)—relationship works but code organization is unconventional
2. **Plain-text password handling**: Passwords stored/validated as plain strings (no hashing)—security risk
3. **Hard-coded database credentials**: Connection string in `database.py` (should use env vars)
4. **Gemini AI endpoint**: `apis/ai.py` has placeholder endpoint (`https://api.gemini.com/v1/process-task`)—needs configuration
5. **Error handling inconsistency**: Some endpoints return dict errors, others raise `HTTPException`

### Validation Patterns

- Mobile: 10-digit numeric strings only (checked in `UserCreate` validator)
- Email: Simple regex check for `@` and `.` (checked in `UserCreate` validator)
- Task creation auto-generates unique `code` field (sequential integer from last task)

## Integration Points

1. **Frontend**: React/Next.js on `localhost:3000` (CORS enabled for this origin)
2. **Gemini AI**: `send_task_to_gemini()` in `apis/ai.py` called from task creation (currently stubbed)
3. **Database**: All queries via `db: Session` dependency; no raw SQL used

## When Adding Features

1. **New entity**: Create model in `models/`, schema in `apis/schemas/`, router in `apis/`
2. **Update response**: Add corresponding Pydantic schema in `apis/schemas/`
3. **Database changes**: Models auto-sync on app restart; no migrations library (use Alembic if multi-environment DB management needed)
4. **Relationships**: Define via SQLAlchemy `relationship()` and ForeignKey; update both sides for many-to-many
