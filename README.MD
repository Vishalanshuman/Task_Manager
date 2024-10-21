
# FastAPI To-Do Application

This is a FastAPI-based application that implements a basic to-do list with authentication and task management functionalities. It uses JWT for secure authentication and allows users to create, retrieve, update, and delete tasks.

## Features

- **User Registration & Login**: Users can register and login using their username, email, and password.
- **JWT Authentication**: Secured endpoints with JWT-based authentication.
- **Task Management**: Users can create, read, update, delete tasks.
- **Task Filtering**: Tasks can be filtered by status or priority.
- **Sorting**: Tasks can be sorted by due date, priority, or creation date.
- **Pagination**: Implemented for task retrieval.
- **Search**: Users can search for tasks based on title or description.
- **Assignment**: Tasks can be assigned to users (many-to-one relationship).

## Project Structure

```
.
├── app
│   ├── auth.py        # Authentication-related endpoints (Login, Register)
│   ├── tasks.py       # Task management endpoints (CRUD operations, filtering, pagination)
├── config
│   ├── __init__.py    # Database connection and session management
│   ├── auth.py        # JWT generation and authentication-related utilities
│   ├── models.py      # SQLAlchemy models for User and Task
│   ├── schema.py      # Pydantic models for request/response validation
├── main.py            # Main entry point for the FastAPI application
├── Dockerfile         # Docker setup file for containerizing the application
├── docker-compose.yml # Docker Compose setup file for multi-service setup
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Requirements

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- JWT (Python-Jose)
- Docker

## Installation (Without Docker)

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/fastapi-todo-app.git
   cd fastapi-todo-app
   ```

2. **Create a Virtual Environment** (Optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Database**:

   Update the `DATABASE_URL` in `docker-compose.yml` or set up a database of your choice.

5. **Run the Application**:

   ```bash
   uvicorn main:app --reload
   ```

   The application will run on `http://127.0.0.1:8000`.

## Running with Docker

1. **Build and Run the Application Using Docker Compose**:

   Make sure Docker is installed on your machine. To build and start the application using Docker Compose, run:

   ```bash
   docker-compose up --build
   ```

   This will build the Docker image, set up the necessary services (like PostgreSQL), and run the FastAPI application.

2. **Access the Application**:

   Once the Docker containers are up and running, you can access the FastAPI application at:

   ```
   http://localhost:8000
   ```

3. **Stop the Application**:

   To stop the Docker containers, use:

   ```bash
   docker-compose down
   ```

## API Endpoints

### Authentication

- **POST /auth/register/** - Register a new user.
- **POST /auth/login/** - Login with username and password.

### Tasks

- **GET /tasks/** - Retrieve tasks with optional filtering, sorting, pagination.
- **POST /tasks/** - Create a new task.
- **GET /tasks/{id}** - Retrieve a task by ID.
- **PUT /tasks/{id}** - Update a task by ID.
- **DELETE /tasks/{id}** - Delete a task by ID.

## Task Filtering, Sorting, Pagination

- **Filtering**: Filter tasks by `status` and `priority`.
- **Sorting**: Sort tasks by `due_date`, `priority`, or `created_at`.
- **Pagination**: Use `limit` and `offset` query parameters for pagination.

### Example Usage

#### Register User

```bash
curl -X POST "http://127.0.0.1:8000/auth/register/" -H "Content-Type: application/json" -d '{"username": "john", "email": "john@example.com", "password": "secret"}'
```

#### Create Task

```bash
curl -X POST "http://127.0.0.1:8000/tasks/" -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"title": "New Task", "description": "Task description", "priority": "high", "status": "pending"}'
```

