# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

# Fact Checker Application

A community-driven web application for submitting and verifying facts.

## Features

- User registration and authentication
- Create and categorize facts
- Vote on facts (Fact or Fake)
- Add supporting information and URLs
- Dashboard with all submitted facts

## Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Set up environment variables:
```bash
cp .env.example .env
```

3. Run the application locally:
```bash
uv run python run.py
```

The application will be available at http://127.0.0.1:5001

## Production Deployment

Run with gunicorn:
```bash
uv run gunicorn -w 4 -b 0.0.0.0:8000 "app.src:create_app()"
```

## Project Structure

```
├── app/
│   └── src/
│       ├── models/          # Database models
│       ├── routes/          # Application routes
│       ├── static/          # CSS and static files
│       ├── templates/       # HTML templates
│       └── extensions.py    # Flask extensions
├── data-model/              # Database schema
├── planning/                # Requirements documentation
└── run.py                   # Application entry point
```

## Usage

1. Register a new account with your email
2. Login to access the dashboard
3. Create categories for organizing facts
4. Submit facts with supporting evidence
5. Vote on existing facts
6. Add additional supporting information

## License

Apache 2.0
