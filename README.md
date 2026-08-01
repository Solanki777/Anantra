# Anantra

Anantra is a multi-tenant, Django-based Student Management System for colleges. Each college registers and manages its own students, while a separate Super Admin panel reviews and approves college registrations, generates login credentials, and oversees the whole platform.

## Features

### College Admin (per-college)
- **College Self-Registration** — Colleges sign up with institution and principal/administrator details (`accounts/register.html`); no password is set at signup. An email is sent confirming the application is under review.
- **Approval-Gated Login** — Accounts stay locked (`set_unusable_password()`) until a Super Admin approves the college; a temporary password is generated and emailed only after approval.
- **Dashboard Analytics** — Totals for students, departments, and courses, a list of recent admissions, and charts for department distribution, course distribution, and monthly admissions — scoped to the logged-in college only.
- **Student CRUD** — Add, view, edit, and delete student records, including photo uploads, all scoped to the college.
- **Search & Pagination** — Search students by name, enrollment number, email, mobile, course, or department, with paginated results (5 per page).
- **CSV Export** — Export the college's student list to CSV.
- **Bulk Import** — Import students in bulk from an Excel file, with column validation and a results/errors summary (`students/services/excel_import.py`, powered by pandas).
- **QR Codes & ID Cards** — Generate a QR code per student (`students/services/qr_generator.py`) and render/download a printable PDF ID card (`students/services/pdf_generator.py`, powered by xhtml2pdf).
- **Public Verification** — Verify a student's enrollment by scanning/visiting a per-student verification URL.
- **Media Handling** — Student photos, QR codes, and college logos are stored under `media/students/`, `media/qr_codes/`, and `media/college_logos/` respectively, and are cleaned up when records are updated or deleted.
- **Password Reset** — Standard Django email-based password reset flow.

### Super Admin
- **Separate Super Admin Login** — Restricted to `is_superuser` accounts, at `/superadmin/`.
- **Platform Dashboard** — Counts of total/pending/approved/rejected/suspended colleges, recent registrations, a recent-activity feed, and a monthly registration trend chart.
- **College Review Queue** — List pending colleges with today/this-month registration counts, and view full college details.
- **Approve / Reject / Suspend / Restore** — Manage a college's lifecycle; approving a college generates credentials and notifies the college by email.
- **Email Action Links** — Signed, token-based action links (`django.core.signing.TimestampSigner`) allow certain approve/reject actions to be triggered directly from an email.
- **Excel Export** — Export the full colleges list to an Excel workbook (openpyxl).

## Tech Stack

- **Backend:** Django 6.0
- **Database:** SQLite (default, via `db.sqlite3`)
- **Data import/export:** pandas, openpyxl
- **QR codes:** `qrcode`
- **PDF generation:** `xhtml2pdf`
- **Config:** `python-decouple` (reads settings from `.env`)
- **Frontend:** Django templates + custom CSS (`static/css/`)

## Project Structure

```
Anantra/
├── accounts/              # College self-registration, login/logout (college-level users)
├── students/               # Student model, views, forms, templates, and services
│   └── services/            # excel_import.py, qr_generator.py, pdf_generator.py
├── colleges/               # College model, admin, and email notifications
├── superadmin/              # Super Admin auth, dashboard, college review/approval, decorators
├── Anantra/                # Project settings, URLs, WSGI/ASGI config
├── templates/               # Shared/base templates + templates/emails/
├── static/                  # CSS and static images
├── staticfiles/              # Collected static files
├── media/
│   ├── students/              # Uploaded student photos
│   ├── qr_codes/               # Generated student QR codes
│   └── college_logos/          # Uploaded college logos
├── db.sqlite3               # SQLite database
├── requirements.txt
└── manage.py
```

## Data Models

**College** (`colleges/models.py`)

| Field | Type | Notes |
|---|---|---|
| `admin` | OneToOneField(User) | The principal/administrator account for this college |
| `college_name` | CharField | |
| `college_code` | CharField | Unique, auto-generated at registration |
| `email` | EmailField | |
| `phone` | CharField | |
| `website` | URLField | Optional |
| `address` | TextField | |
| `city` / `state` | CharField | |
| `logo` | ImageField | Optional, uploaded to `media/college_logos/` |
| `status` | CharField | `pending` / `approved` / `rejected` / `suspended` |
| `created_at` | DateTimeField | Auto-set on creation |

**Student** (`students/models.py`)

| Field | Type | Notes |
|---|---|---|
| `college` | ForeignKey(College) | Owning college; all queries are scoped to this |
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
pip install -r requirements.txt

# Configure environment variables (see below), then apply migrations
python manage.py migrate

# Create a super admin account (for /superadmin/ access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

### Environment Variables

Settings are loaded via `python-decouple` from a `.env` file in the project root:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

EMAIL_HOST_USER=your-gmail-address@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

Email is sent via Gmail SMTP (`smtp.gmail.com:587`, TLS), so `EMAIL_HOST_USER`/`EMAIL_HOST_PASSWORD` should be a Gmail address and an [app password](https://support.google.com/accounts/answer/185833), not the account's regular password.

## Usage

1. A college **registers** at `/register/` with its institution and administrator details. The account is created but locked, and a confirmation email is sent.
2. A **Super Admin** logs in at `/superadmin/`, reviews the college under **Pending Colleges**, and **approves** it — this issues login credentials and emails them to the college.
3. The college's administrator **logs in** at `/login/` (redirects to the **dashboard** at `/dashboard/`).
4. From the dashboard, add students at `/add/`, browse/search them at `/students/`, and edit/delete/view details per row.
5. Use `/import/` to bulk-import students from an Excel file, `/export/csv/` to export the current list, and `/id-card/<id>/` to generate a QR-coded ID card (downloadable as PDF at `/id-card/<id>/download/`).
6. Anyone can verify a student's enrollment via `/verify/<enrollment_no>/`.
7. **Log out** at `/logout/`.

## URL Routes

### College / Student Management (public site)

| URL | View | Description |
|---|---|---|
| `/` | `home` | Landing page |
| `/register/` | `register_view` | College self-registration |
| `/login/` | `login_view` | College administrator login |
| `/logout/` | `logout_view` | Logout (login required) |
| `/dashboard/` | `dashboard` | College analytics dashboard (login required) |
| `/add/` | `add_student` | Add a new student (login required) |
| `/students/` | `student_list` | List/search students (login required) |
| `/edit/<id>/` | `edit_student` | Edit a student (login required) |
| `/delete/<id>/` | `delete_student` | Delete a student (login required) |
| `/show/<id>/` | `show_details` | View student details (login required) |
| `/export/csv/` | `export_student_csv` | Export students to CSV (login required) |
| `/import/` | `import_students` | Bulk-import students from Excel (login required) |
| `/verify/<enrollment_no>/` | `verify_student` | Public enrollment verification |
| `/id-card/<id>/` | `generate_id_card` | Generate a student ID card with QR (login required) |
| `/id-card/<id>/download/` | `download_id_card` | Download the ID card as PDF (login required) |
| `/password-reset/` … `/reset-complete/` | Django auth views | Standard password-reset flow |
| `/admin/` | Django admin | Admin panel |

### Super Admin (`/superadmin/`)

| URL | View | Description |
|---|---|---|
| `/superadmin/` | `login_view` | Super Admin login |
| `/superadmin/logout/` | `logout_view` | Super Admin logout |
| `/superadmin/dashboard/` | `dashboard` | Platform-wide analytics |
| `/superadmin/pending/` | `pending_colleges` | Colleges awaiting approval |
| `/superadmin/colleges/` | `list_colleges` | All colleges |
| `/superadmin/colleges/<status>/` | `list_colleges` | Colleges filtered by status |
| `/superadmin/college/<id>/` | `college_details` | College detail view |
| `/superadmin/college/<id>/approve/` | `approve_college` | Approve a college & issue credentials |
| `/superadmin/college/<id>/reject/` | `reject_college` | Reject a college |
| `/superadmin/college/<id>/suspend/` | `suspend_college` | Suspend an approved college |
| `/superadmin/college/<id>/restore/` | `restore_college` | Restore a suspended college |
| `/superadmin/college/<id>/view/` | `college_view` | Read-only college view |
| `/superadmin/college/<id>/edit/` | `edit_college` | Edit college details |
| `/superadmin/colleges/export/` | `export_colleges_excel` | Export all colleges to Excel |
| `/superadmin/action/<action>/<college_id>/<token>/` | `email_action` | Signed one-click approve/reject link from email |

## Notes

- `LOGIN_URL` is set to `login`, so unauthenticated access to college-side protected views redirects to `/login/`; Super Admin views are protected separately via the `@superadmin_required` decorator (`superadmin/decorators.py`).
- All student data is tenant-scoped: views filter by `request.user.college`, so one college cannot see or modify another college's students.
- In development (`DEBUG=True`), uploaded media files are served automatically via Django's static file helper.
- A `.env` file is required for the app to start (`SECRET_KEY`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `ALLOWED_HOSTS`); do not commit real credentials.

## License

No license file is included. Add one if you plan to distribute this project.