# Client-Order System

A simple **Django-based web application** for managing clients and orders. This project allows you to:

- Manage clients (add, edit, view, delete)
- Manage orders (add, edit, track status, view recent orders)
- Export clients and orders as CSV
- View a dashboard with order summaries

---

## Features

- **Client Management**: Store client information including name, email, phone, and company.
- **Order Management**: Track order details, amount, status, and assigned user.
- **Dashboard**: Summary of total clients, orders, and order statuses.
- **CSV Export**: Export client and order lists for reporting.
- **Authentication**: Admin/staff login required for protected views.

---

## Tech Stack

- **Backend**: Django 4.x  
- **Database**: SQLite (default)  
- **Frontend**: Bootstrap 5 + Django Templates  
- **Authentication**: Django’s built-in user authentication

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/WM0307/client-order-system.git
cd client-order-system
```

2. (Optional) Create a virtual environment

```bash
python -m venv .venv
```
Activate it

- Windows
```bash
.venv\Scripts\activate
```

- Mac/Linux
```bash
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply migrations

```bash
python manage.py migrate
```

5. Load sample data (fixtures)

```bash
python manage.py loaddata orders/fixtures/sample_data.json
```

6. Create superuser for admin access

```bash
python manage.py createsuperuser
```

7. Run the development server

```bash
python manage.py runserver
```

Access the site at http://127.0.0.1:8000
Admin panel at http://127.0.0.1:8000/admin

## Running Tests
Unit tests are included for models and views

```bash
python manage.py test
```

Tests cover:
- User authentication
- Creating clients and orders
- Loading list views
- CSV export functionality
Unit tests use a test database and do not affect your main database.