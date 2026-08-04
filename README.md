# Notes API (Flask + Session Auth)

A simple, Flask REST API for a personal Notes app.
Uses session-based authentication (cookies) and SQLite via SQLAlchemy.

## Tech Stack

- Python 3.8+
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-RESTful 0.3.9
- Flask-Bcrypt 1.0.1
- Flask-Migrate 4.0.0
- Marshmallow 3.20.1

## Project Structure

```
project_root/
│── app.py
│── config.py
|── migrations/
    |── versions/
        |── 3b1f04ae6184_initial_migration_users_and_notes.py
    |── alembic.ini
    |── env.py
    |── README
    |── script.py.mako
│── seed.py
|── app.db
|── .gitignore
│── models/
│   ├── __init__.py
│   ├── db.py
│   ├── user.py
│   ├── note.py
│   └── schemas.py
│── Pipfile
|── Pipfile.lock
└── README.md
```

## Setup & Running (terminal commands)

Run these in order from the project root.

### 1. Install dependencies

```bash
pipenv install
pipenv shell
```

### 2. Set up the database with Flask-Migrate

```bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration users and notes"
flask db upgrade
```

(On Windows use `set FLASK_APP=app.py` instead of `export`.)

### 3. Seed the database with fake data

```bash
python seed.py
```

This clears any existing data and creates 5 fake users (password:
`password123` for all of them), each with 4 notes.

### 4. Run the server

```bash
python app.py
```

The API will be running at `http://localhost:5555`.

## API Endpoints

### Auth

| Method | Route            | Description                          |
|--------|-------------------|---------------------------------------|
| POST   | `/signup`          | Create a new user, logs them in       |
| POST   | `/login`           | Log in with username + password       |
| DELETE | `/logout`          | Log out the current user              |
| GET    | `/check_session`   | Check who (if anyone) is logged in    |

**Signup / Login body example:**
```json
{
  "username": "arnold",
  "password": "password123"
}
```

### Notes (all require being logged in)

| Method | Route              | Description                              |
|--------|---------------------|--------------------------------------------|
| GET    | `/notes?page=1&per_page=5` | Paginated list of your notes       |
| POST   | `/notes`            | Create a new note                          |
| PATCH  | `/notes/<id>`       | Update a note you own                      |
| DELETE | `/notes/<id>`       | Delete a note you own                      |

**Create note body example:**
```json
{
  "title": "Groceries",
  "content": "Milk, eggs, bread"
}
```

### Status Codes to Expect

- `401 Unauthorized` — you're not logged in
- `403 Forbidden` — you're logged in, but trying to touch someone else's note
- `404 Not Found` — the note id doesn't exist
- `422 Unprocessable Entity` — validation failed (bad/missing fields)

## Notes on Authentication

This app uses Flask's built-in `session` (a signed cookie), not tokens.
When testing with something like Postman or Insomnia, make sure
"cookies" / "session" persistence is turned on between requests, or
login will appear to "not stick."
