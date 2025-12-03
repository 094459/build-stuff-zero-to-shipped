# Fact Checking Application Requirements

## Ubiquitous Requirements (always active)
- The system SHALL use the data model defined in "data-model/fact-checker.sql"
- The system SHALL be a web application accessible via browser
- The system SHALL provide a simple web design that can be updated easily using CSS

## Event-Driven Requirements (WHEN trigger THEN response)
- WHEN a user successfully logs in, THEN the system SHALL display a Dashboard
- WHEN the Dashboard is displayed, THEN the system SHALL show a simple explanation of what the application does
- WHEN the Dashboard is displayed, THEN the system SHALL display all available Facts that have been created
- WHEN a user clicks on an existing Fact, THEN the system SHALL display the Fact details view
- WHEN a user is viewing a Fact, THEN the system SHALL display two buttons labeled "Fact" and "Fake"
- WHEN a user clicks the "Fact" or "Fake" button, THEN the system SHALL record their vote
- WHEN a user clicks "Create a new Fact" from the Dashboard, THEN the system SHALL display a Fact creation form
- WHEN a user clicks "Create a new Category" from the Dashboard, THEN the system SHALL display a Category creation form

## State-Driven Requirements (WHILE condition THEN response)
- WHILE a user is viewing a Fact, the system SHALL provide the ability to add supporting information

## Unwanted Behavior (IF condition THEN response)
- IF a user is not registered, THEN the system SHALL require them to register with an email address before login
- IF a user is not logged in, THEN the system SHALL NOT display the Dashboard

## Optional Features (WHERE condition THEN response)
- WHERE a Fact has supporting information, the system SHALL display it on the Fact details view

## Complex Requirements (additional clarifications)
- The Dashboard SHALL provide navigation options to:
  - View existing Facts (clickable list)
  - Create a new Fact (button/link)
  - Create a new Category (button/link)

## Areas Requiring Further Clarification

### User Registration & Authentication
- Password requirements (minimum length, complexity)
- Post-registration behavior (auto-login or redirect to login?)
- Password reset functionality needed?
- Email verification required?

### Voting System
- Should vote counts be displayed on Facts?
- Can users change their vote?
- Should voting be anonymous or attributed?
- Display vote ratio/percentage?

### Supporting Information
- How is supporting info added? (text field, form, modal?)
- Can multiple users add supporting info or only the Fact creator?
- Should supporting info be versioned/timestamped?
- Character limits on supporting info?

### Fact Creation Form
- Required fields: content, category, supporting_url, supporting_info?
- Validation rules for URLs?
- Character limits on content?

### Category Creation Form
- Required fields: name, description?
- Who can create categories (all users or admins only)?
- Duplicate category name handling?

### Dashboard Display
- Sort order for Facts (newest first, most voted, etc.)?
- Pagination needed for large number of Facts?
- Filter by category?
- Search functionality?
