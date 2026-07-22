# Anantra

Anantra is a Django-based Student Management System designed to simplify student record management through a secure web interface. It provides user authentication, dashboard analytics, CRUD operations, and search functionality using Django ORM.

## Features

- **User Authentication** — Register, log in, and log out with Django's built-in auth system (custom registration form with email field).
- **Dashboard Analytics** — At-a-glance stats for total students, departments, and courses, plus charts for department distribution, course distribution, and monthly admissions.
- **Student CRUD** — Add, view, edit, and delete student records, including photo uploads.
- **Search & Pagination** — Search students by name, enrollment number, email, mobile, course, or department, with paginated results (5 per page).
- **CSV Export** — Export the full student list to a CSV file.
- **Media Handling** — Student photos are stored under `media/students/` and automatically removed when a record is updated with a new photo or deleted.

## Tech Stack

- **Backend:** Django 6.0
- **Database:** SQLite (default, via `db.sqlite3`)
- **Image handling:** Pillow
- **Frontend:** Django templates + custom CSS (`static/css/style.css`)

## Project Structure

```
Anantra/
├── accounts/            # Authentication app (register, login, logout)
├── students/            # Core app: student model, views, forms, templates
├── Anantra/            # Project settings, URLs, WSGI/ASGI config
├── templates/            # Shared/base templates
├── static/               # CSS and static images
├── media/students/       # Uploaded student photos
├── db.sqlite3            # SQLite database
└── manage.py
```

## Data Model

**Student** (`students/models.py`)

| Field | Type | Notes |
|---|---|---|
| `name` | CharField | Student's full name |
| `enrollment_no` | CharField | Unique, optional |
| `semester` | PositiveSmallIntegerField | Choices: Semester 1–8 |
| `email` | EmailField | Unique |
| `mobile` | CharField | |
| `course` | CharField | |
| `department` | CharField | |
| `admission_date` | DateField | |
| `photo` | ImageField | Optional, uploaded to `media/students/` |

## Getting Started

### Prerequisites

- Python 3.13+
- pip

### Installation

```bash
# Clone or extract the project, then move into it
cd Anantra

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install django pillow

# Apply migrations
python manage.py migrate

# Create an admin user (optional, for /admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Usage

1. **Register** a new account at `/register/`, then **log in** at `/login/`.
2. After logging in, you're redirected to the **dashboard** (`/dashboard/`) with summary stats and charts.
3. Use **Add Student** (`/add/`) to create new records.
4. Browse and search records at **Student List** (`/students/`), with edit/delete/detail actions per row.
5. Export the current student list as CSV via `/export/csv/`.
6. **Log out** at `/logout/`.

## URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `home` | Landing page |
| `/dashboard/` | `dashboard` | Analytics dashboard (login required) |
| `/add/` | `add_student` | Add a new student (login required) |
| `/students/` | `student_list` | List/search students (login required) |
| `/edit/<id>/` | `edit_student` | Edit a student (login required) |
| `/delete/<id>/` | `delete_student` | Delete a student (login required) |
| `/show/<id>/` | `show_details` | View student details (login required) |
| `/export/csv/` | `export_student_csv` | Export students to CSV (login required) |
| `/register/` | `register_view` | User registration |
| `/login/` | `login_view` | User login |
| `/logout/` | `logout_view` | User logout (login required) |
| `/admin/` | Django admin | Admin panel |

## Notes

- `LOGIN_URL` is set to `login`, so unauthenticated access to protected views redirects to the login page.
- In development (`DEBUG=True`), uploaded media files are served automatically via Django's static file helper.
- No `requirements.txt` was found in the project; install `django` and `pillow` manually as shown above, or generate one from the bundled `venv` with `pip freeze > requirements.txt`.

## License

No license file is included. Add one if you plan to distribute this project.