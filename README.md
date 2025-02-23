# 📝 Task Manager API

## 🚀 Overview
The **Task Manager API** is a Django REST Framework (DRF) application that allows users to **manage tasks** with authentication and role-based access. 
It supports **user registration, task management, authentication via JWT tokens, and API documentation using Swagger**.

## 📌 Features
- User Authentication (Register, Login, Logout using JWT)
- Task CRUD Operations (Create, Read, Update, Delete)
- Filtering & Searching (Filter tasks by status, priority, and assigned_to)
- Django Signals (Send email notifications on task assignments)
- Token-Based Authentication (JWT-based authentication with Django REST Framework)
- Throttling (Rate limiting for API requests)
- Swagger API Documentation

## 📦 Installation & Setup
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Set Up Environment Variables

Create a **.env** file in the root directory:
```bash
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```
### 5. Apply Migrations
```bash
python manage.py migrate
python manage.py createsuperuser  # Create an admin user
```
### 6. python manage.py runserver
```bash
python manage.py runserver
```
API will be available at: `http://127.0.0.1:8000/`
##
## 🔑 Authentication
This API uses JWT authentication for securing endpoints.

## Obtain a Token
```bash
POST /api/token/
```
**Request Body:**

```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response:**

```json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
```

### Use the Access Token for Authentication

Include the token in the `Authorization` header:

```http
Authorization: Bearer your_access_token
```

### Refresh the Token

```http
POST /api/token/refresh/
```

### Logout (Blacklist Token)

```http
POST /api/logout/
```

**Request Body:**

```json
{
  "refresh": "your_refresh_token"
}
```

---

## 📚 API Endpoints

### 🏷️ **User Endpoints**

| Method | Endpoint              | Description              |
| ------ | --------------------- | ------------------------ |
| POST   | `/api/users/`         | Register a new user      |
| POST   | `/api/token/`         | Obtain JWT token         |
| POST   | `/api/token/refresh/` | Refresh JWT token        |
| POST   | `/api/logout/`        | Logout & blacklist token |

### 🏷️ **Task Endpoints**

| Method | Endpoint           | Description           |
| ------ | ------------------ | --------------------- |
| GET    | `/api/tasks/`      | List all tasks        |
| POST   | `/api/tasks/`      | Create a new task     |
| GET    | `/api/tasks/{id}/` | Retrieve task details |
| PUT    | `/api/tasks/{id}/` | Update a task         |
| DELETE | `/api/tasks/{id}/` | Delete a task         |

---

## 📊 API Documentation

Swagger API docs are available at:

- **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## 🛠️ Running Tests

Use **pytest** to run tests:

```sh
pytest
```

Run specific tests:

```sh
pytest tasks/tests/test_taskviewset.py -v
```

---

## 🚀 Deployment

### 1 Collect Static Files

```sh
python manage.py collectstatic
```

### 2 Deploy to Production (e.g., Heroku, AWS, DigitalOcean)

- Use **Gunicorn** as WSGI server
- Configure **PostgreSQL database**
- Set up **environment variables**

Example **Gunicorn command**:

```sh
gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request 

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 📬 Contact

For any questions, reach out via:
📧 **Email**: [danogbans@gmail.com](mailto\:danogbans@gmail.com)\
🔗 **GitHub**: [github.com/Danogbans](https://github.com/Danogbans)

