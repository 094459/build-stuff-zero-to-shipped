# Book Sharing Application

A web application for sharing books with friends and community members.

## Features

- Public dashboard showing available books with filtering options
  - Filter by availability (all books or available books)
  - Filter by category (fiction or non-fiction)
- User registration with invite code system
- User profiles with personal book collections
- Book management (create, edit, view, hide/show)
- Book categorization (fiction/non-fiction)
- Book comments and upvotes system
- Book borrowing system with request/approval workflow
- Borrowing history tracking

## Technology Stack

- Flask web framework
- SQLAlchemy ORM
- Flask-Login for authentication
- Flask-WTF for forms and CSRF protection
- Bootstrap 5 for UI
- SQLite database (configurable for other databases)

## Project Structure

```
src/
├── static/          # Static assets (CSS, JS, images)
├── models/          # Database models
├── routes/          # Route handlers
├── templates/       # HTML templates
├── forms/           # Form definitions
├── extensions.py    # Flask extensions
├── app.py           # Application factory
data-model/          # Database schema documentation
migrations/          # Database migrations
```

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`
5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. Run the application:
   ```
   flask run
   ```

## Initial Setup

The application creates an initial invite code (`INITIAL`) that can be used for the first user registration.

## Running with Gunicorn (Production)

To run the application in a production environment with Gunicorn:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application using Gunicorn:
   ```
   gunicorn -c gunicorn_config.py wsgi:application
   ```

   Or simply:
   ```
   gunicorn wsgi:application
   ```

3. For platforms like Heroku, a Procfile is included:
   ```
   web: gunicorn -c gunicorn_config.py wsgi:application
   ```

The Gunicorn configuration can be customized by editing `gunicorn_config.py` or by setting environment variables.

## UML Sequence Diagrams

### 1. User Registration and Login Process

```
┌─────────┐          ┌────────────┐          ┌────────────┐          ┌────────────┐
│  User   │          │   Browser  │          │Flask Server│          │  Database  │
└────┬────┘          └─────┬──────┘          └─────┬──────┘          └─────┬──────┘
     │                     │                       │                       │
     │  Visit Register     │                       │                       │
     │  Page               │                       │                       │
     │ ──────────────────> │                       │                       │
     │                     │  GET /auth/register   │                       │
     │                     │ ──────────────────────>                       │
     │                     │                       │                       │
     │                     │  Return Register Form │                       │
     │                     │ <──────────────────────                       │
     │                     │                       │                       │
     │  Fill Form with     │                       │                       │
     │  Email, Password,   │                       │                       │
     │  and Invite Code    │                       │                       │
     │ ──────────────────> │                       │                       │
     │                     │  POST /auth/register  │                       │
     │                     │ ──────────────────────>                       │
     │                     │                       │  Validate Invite Code │
     │                     │                       │ ──────────────────────>
     │                     │                       │                       │
     │                     │                       │  Code Valid/Invalid   │
     │                     │                       │ <──────────────────────
     │                     │                       │                       │
     │                     │                       │  If Valid: Create User│
     │                     │                       │ ──────────────────────>
     │                     │                       │                       │
     │                     │                       │  User Created         │
     │                     │                       │ <──────────────────────
     │                     │                       │                       │
     │                     │                       │  Generate Personal    │
     │                     │                       │  Invite Code          │
     │                     │                       │ ──────────────────────>
     │                     │                       │                       │
     │                     │                       │  Code Generated       │
     │                     │                       │ <──────────────────────
     │                     │                       │                       │
     │                     │  Redirect to Login    │                       │
     │                     │ <──────────────────────                       │
     │                     │                       │                       │
     │  Visit Login Page   │                       │                       │
     │ ──────────────────> │                       │                       │
     │                     │  GET /auth/login      │                       │
     │                     │ ──────────────────────>                       │
     │                     │                       │                       │
     │                     │  Return Login Form    │                       │
     │                     │ <──────────────────────                       │
     │                     │                       │                       │
     │  Enter Email and    │                       │                       │
     │  Password           │                       │                       │
     │ ──────────────────> │                       │                       │
     │                     │  POST /auth/login     │                       │
     │                     │ ──────────────────────>                       │
     │                     │                       │  Verify Credentials   │
     │                     │                       │ ──────────────────────>
     │                     │                       │                       │
     │                     │                       │  Valid/Invalid        │
     │                     │                       │ <──────────────────────
     │                     │                       │                       │
     │                     │                       │  Create Session       │
     │                     │                       │ ──────────────────────>
     │                     │                       │                       │
     │                     │  Redirect to Dashboard│                       │
     │                     │ <──────────────────────                       │
     │                     │                       │                       │
     │  View Dashboard     │                       │                       │
     │ <─────────────────── │                       │                       │
     │                     │                       │                       │
```

### 2. Adding Books Process

```
┌─────────┐          ┌────────────┐          ┌────────────┐          ┌────────────┐
│  User   │          │   Browser  │          │Flask Server│          │  Database  │
└────┬────┘          └─────┬──────┘          └─────┬──────┘          └─────┬──────┘
     │                     │                       │                       │
     │  Click "Add Book"   │                       │                       │
     │ ──────────────────> │                       │                       │
     │                     │  GET /books/create    │                       │
     │                     │ ──────────────────────>                       │
     │                     │                       │                       │
     │                     │  Return Book Form     │                       │
     │                     │ <──────────────────────                       │
     │                     │                       │                       │
     │  Fill Book Details  │                       │                       │
     │  (Title, Author,    │                       │                       │
     │   Fiction/Non-      │                       │                       │
     │   Fiction, etc.)    │                       │                       │
     │ ──────────────────> │                       │                       │
     │                     │  POST /books/create   │                       │
     │                     │ ──────────────────────>                       │
     │                     │                       │                       │
     │                     │                       │  Validate Form Data   │
     │                     │                       │ ─────────────────────┐│
     │                     │                       │                      ││
     │                     │                       │ <─────────────────────┘│
     │                     │                       │                       │
     │                     │                       │  Create Book Record   │
     │                     │                       │ ──────────────────────>
     │                     │                       │                       │
     │                     │                       │  Book Created         │
     │                     │                       │ <──────────────────────
     │                     │                       │                       │
     │                     │  Redirect to Book View│                       │
     │                     │ <──────────────────────                       │
     │                     │                       │                       │
     │  View Book Details  │                       │                       │
     │ <─────────────────── │                       │                       │
     │                     │                       │                       │
     │  Add Comment        │                       │                       │
     │  (Optional)         │                       │                       │
     │ ──────────────────> │                       │                       │
     │                     │  POST /books/{id}/    │                       │
     │                     │  comment              │                       │
     │                     │ ──────────────────────>                       │
     │                     │                       │  Save Comment         │
     │                     │                       │ ──────────────────────>
     │                     │                       │                       │
     │                     │                       │  Comment Saved        │
     │                     │                       │ <──────────────────────
     │                     │                       │                       │
     │                     │  Refresh Book View    │                       │
     │                     │ <──────────────────────                       │
     │                     │                       │                       │
     │  Toggle Visibility  │                       │                       │
     │  (Optional)         │                       │                       │
     │ ──────────────────> │                       │                       │
     │                     │  POST /books/{id}/    │                       │
     │                     │  toggle-visibility    │                       │
     │                     │ ──────────────────────>                       │
     │                     │                       │  Update Visibility    │
     │                     │                       │ ──────────────────────>
     │                     │                       │                       │
     │                     │                       │  Updated              │
     │                     │                       │ <──────────────────────
     │                     │                       │                       │
     │                     │  Redirect to My Books │                       │
     │                     │ <──────────────────────                       │
     │                     │                       │                       │
```

### 3. Borrowing and Returning Books Process

```
┌─────────┐          ┌────────────┐          ┌────────────┐          ┌────────────┐          ┌────────────┐
│ Borrower│          │   Browser  │          │Flask Server│          │  Database  │          │Book Owner  │
└────┬────┘          └─────┬──────┘          └─────┬──────┘          └─────┬──────┘          └─────┬──────┘
     │                     │                       │                       │                       │
     │  View Book Details  │                       │                       │                       │
     │ ──────────────────> │                       │                       │                       │
     │                     │  GET /books/{id}      │                       │                       │
     │                     │ ──────────────────────>                       │                       │
     │                     │                       │  Get Book Details     │                       │
     │                     │                       │ ──────────────────────>                       │
     │                     │                       │                       │                       │
     │                     │                       │  Return Book Data     │                       │
     │                     │                       │ <──────────────────────                       │
     │                     │                       │                       │                       │
     │                     │  Display Book with    │                       │                       │
     │                     │  "Request to Borrow"  │                       │                       │
     │                     │ <──────────────────────                       │                       │
     │                     │                       │                       │                       │
     │  Click "Request     │                       │                       │                       │
     │  to Borrow"         │                       │                       │                       │
     │ ──────────────────> │                       │                       │                       │
     │                     │  POST /books/{id}/    │                       │                       │
     │                     │  request-borrow       │                       │                       │
     │                     │ ──────────────────────>                       │                       │
     │                     │                       │  Create Borrow Request│                       │
     │                     │                       │ ──────────────────────>                       │
     │                     │                       │                       │                       │
     │                     │                       │  Request Created      │                       │
     │                     │                       │ <──────────────────────                       │
     │                     │                       │                       │                       │
     │                     │  Redirect to Requests │                       │                       │
     │                     │  Page                 │                       │                       │
     │                     │ <──────────────────────                       │                       │
     │                     │                       │                       │                       │
     │                     │                       │                       │                       │
     │                     │                       │                       │                       │
     │                     │                       │                       │  Owner Logs In        │
     │                     │                       │                       │ <─────────────────────│
     │                     │                       │                       │                       │
     │                     │                       │                       │  View Borrow Requests │
     │                     │                       │                       │ <─────────────────────│
     │                     │                       │                       │                       │
     │                     │                       │  GET /profile/requests│                       │
     │                     │                       │ <─────────────────────────────────────────────│
     │                     │                       │                       │                       │
     │                     │                       │  Get Pending Requests │                       │
     │                     │                       │ ──────────────────────>                       │
     │                     │                       │                       │                       │
     │                     │                       │  Return Requests      │                       │
     │                     │                       │ <──────────────────────                       │
     │                     │                       │                       │                       │
     │                     │                       │  Display Requests     │                       │
     │                     │                       │ ─────────────────────────────────────────────>│
     │                     │                       │                       │                       │
     │                     │                       │                       │  Approve Request      │
     │                     │                       │                       │ <─────────────────────│
     │                     │                       │                       │                       │
     │                     │                       │  POST /books/request/ │                       │
     │                     │                       │  {id}/approve         │                       │
     │                     │                       │ <─────────────────────────────────────────────│
     │                     │                       │                       │                       │
     │                     │                       │  Update Request Status│                       │
     │                     │                       │  & Book Availability  │                       │
     │                     │                       │ ──────────────────────>                       │
     │                     │                       │                       │                       │
     │                     │                       │  Create Borrow History│                       │
     │                     │                       │ ──────────────────────>                       │
     │                     │                       │                       │                       │
     │                     │                       │  Updated              │                       │
     │                     │                       │ <──────────────────────                       │
     │                     │                       │                       │                       │
     │                     │                       │  Redirect to Requests │                       │
     │                     │                       │ ─────────────────────────────────────────────>│
     │                     │                       │                       │                       │
     │  View Borrowed Book │                       │                       │                       │
     │ ──────────────────> │                       │                       │                       │
     │                     │  GET /profile/borrowed│                       │                       │
     │                     │ ──────────────────────>                       │                       │
     │                     │                       │  Get Borrowed Books   │                       │
     │                     │                       │ ──────────────────────>                       │
     │                     │                       │                       │                       │
     │                     │                       │  Return Books         │                       │
     │                     │                       │ <──────────────────────                       │
     │                     │                       │                       │                       │
     │                     │  Display Borrowed     │                       │                       │
     │                     │  Books               │                       │                       │
     │                     │ <──────────────────────                       │                       │
     │                     │                       │                       │                       │
     │  Return Book        │                       │                       │                       │
     │ ──────────────────> │                       │                       │                       │
     │                     │  POST /books/{id}/    │                       │                       │
     │                     │  return               │                       │                       │
     │                     │ ──────────────────────>                       │                       │
     │                     │                       │  Update Book Status   │                       │
     │                     │                       │  & Borrowing History  │                       │
     │                     │                       │ ──────────────────────>                       │
     │                     │                       │                       │                       │
     │                     │                       │  Updated              │                       │
     │                     │                       │ <──────────────────────                       │
     │                     │                       │                       │                       │
     │                     │  Redirect to Dashboard│                       │                       │
     │                     │ <──────────────────────                       │                       │
     │                     │                       │                       │                       │
```

## License

MIT
