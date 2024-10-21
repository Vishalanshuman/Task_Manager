
# Todo List API

This is a simple To-Do List API built using FastAPI and SQLAlchemy. The API supports CRUD operations, including creating, reading, updating, and deleting tasks, with pagination for retrieving tasks.

## Features
- Create a new task (To-Do).
- Get all tasks with pagination support.
- Get a specific task by ID.
- Update a task by ID.
- Delete a task by ID.

## Project Structure

```bash
├── app.py                # Main FastAPI app
├── config.py             # Database configuration and SQLAlchemy models
├── README.md             # Project documentation (this file)
├── requirements.txt      # Python dependencies
```

## Getting Started

### Prerequisites
To run this project, you'll need:
- Python 3.7+
- FastAPI
- SQLAlchemy
- PostgreSQL (or SQLite)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/todo-api.git
cd todo-api
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up your database:**
   - Configure your database settings in `config.py`. By default, this project uses a local SQLite database, but you can switch to PostgreSQL or any other relational database supported by SQLAlchemy.

4. **Run the application:**

```bash
uvicorn app:app --reload
```

The API will now be available at `http://127.0.0.1:8000`.

### API Endpoints

#### 1. Create a New Task

- **URL:** `/tasks/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "title": "Buy groceries",
    "description": "Milk, Bread, Cheese",
    "priority": "high",
    "status": "pending",
    "due_date": "2024-10-21"
  }
  ```
- **Response:** Returns the created task.

#### 2. Get All Tasks (With Pagination)

- **URL:** `/tasks/`
- **Method:** `GET`
- **Query Params:** 
  - `skip`: Number of tasks to skip (default: `0`)
  - `limit`: Number of tasks to return (default: `10`)
- **Response:**
  ```json
  {
    "total": 100,
    "skip": 0,
    "limit": 10,
    "todos": [
      {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Bread, Cheese",
        "priority": "high",
        "status": "pending",
        "due_date": "2024-10-21"
      }
    ]
  }
  ```

#### 3. Get Task by ID

- **URL:** `/tasks/{task_id}`
- **Method:** `GET`
- **Response:** Returns the task with the given ID.

#### 4. Update Task by ID

- **URL:** `/tasks/{task_id}`
- **Method:** `PUT`
- **Request Body:** (Partial updates are supported)
  ```json
  {
    "title": "Buy groceries and snacks",
    "status": "inprogress"
  }
  ```
- **Response:** Returns the updated task.

#### 5. Delete Task by ID

- **URL:** `/tasks/{task_id}`
- **Method:** `DELETE`
- **Response:** Returns a message confirming task deletion.

### Database Models

- **Todo Model:**
  ```python
  class Todo(Base):
      __tablename__ = "todos"

      id = Column(Integer, primary_key=True, index=True)
      title = Column(String, index=True)
      description = Column(String)
      priority = Column(String)
      status = Column(String)
      due_date = Column(Date)
  ```

- **TodoCreate Schema:**
  ```python
  class TodoCreate(BaseModel):
      title: str
      description: str
      priority: str
      status: str
      due_date: date
  ```

- **TodoUpdate Schema:**
  ```python
  class TodoUpdate(BaseModel):
      title: Optional[str]
      description: Optional[str]
      priority: Optional[str]
      status: Optional[str]
      due_date: Optional[date]
  ```

- **TodoOutput Schema:**
  ```python
  class TodoOutput(BaseModel):
      id: int
      title: str
      description: str
      priority: str
      status: str
      due_date: date

      class Config:
          orm_mode = True
  ```

### Error Handling
- If a task is not found (404): 
  ```json
  {
    "detail": "Task Not Found"
  }
  ```

### Testing

You can test the API using [Postman](https://www.postman.com/) or [curl](https://curl.se/). For example, to create a new task:

```bash
curl -X POST "http://127.0.0.1:8000/tasks/" -H "Content-Type: application/json" -d '{"title": "Buy groceries", "description": "Milk, Bread, Cheese", "priority": "high", "status": "pending", "due_date": "2024-10-21"}'
```


Enjoy building your To-Do list API! If you have any questions, feel free to reach out.
