# Implementation Plan

- [ ] 1. Set up project structure and dependencies
  - Create directory structure: src/, src/models/, src/routes/, src/templates/, src/static/css/
  - Initialize uv project with pyproject.toml
  - Add Flask, Flask-SQLAlchemy, Flask-Login, Pydantic, and Gunicorn dependencies
  - Create src/__init__.py with application factory pattern
  - Create src/extensions.py for Flask extension initialization
  - Create src/config.py with development and production configurations
  - _Requirements: All_

- [ ] 2. Implement database models
  - Create src/models/__init__.py
  - Implement User model with email, password_hash, and password methods
  - Implement Category model with name field
  - Implement Fact model with title, description, category relationship, and creator relationship
  - Implement Evaluation model with fact relationship, user relationship, is_true boolean, and supporting_info
  - Configure SQLAlchemy relationships between models
  - _Requirements: 1.1, 1.4, 4.1, 4.4, 5.1, 6.2, 6.3, 6.4, 7.2_

- [ ]* 2.1 Write property test for password hashing
  - **Property 3: Password hashing security**
  - **Validates: Requirements 1.4**

- [ ]* 2.2 Write unit tests for model relationships
  - Test User-Fact relationship
  - Test Category-Fact relationship
  - Test Fact-Evaluation relationship
  - Test User-Evaluation relationship
  - _Requirements: 4.1, 6.2, 6.3_

- [ ] 3. Implement authentication routes and templates
  - Create src/routes/auth.py blueprint
  - Implement GET /register route with registration form template
  - Implement POST /register route with email validation and user creation
  - Implement GET /login route with login form template
  - Implement POST /login route with authentication logic
  - Implement GET /logout route with session termination
  - Create src/templates/auth/register.html with semantic HTML and CSS classes
  - Create src/templates/auth/login.html with semantic HTML and CSS classes
  - Configure Flask-Login user loader
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.4_

- [ ]* 3.1 Write property test for valid registration
  - **Property 1: Valid registration creates user account**
  - **Validates: Requirements 1.1**

- [ ]* 3.2 Write property test for invalid email rejection
  - **Property 2: Invalid email formats are rejected**
  - **Validates: Requirements 1.2**

- [ ]* 3.3 Write property test for valid authentication
  - **Property 4: Valid credentials authenticate successfully**
  - **Validates: Requirements 2.1, 2.3**

- [ ]* 3.4 Write property test for invalid credentials rejection
  - **Property 5: Invalid credentials are rejected**
  - **Validates: Requirements 2.2**

- [ ]* 3.5 Write property test for logout session termination
  - **Property 6: Logout terminates session**
  - **Validates: Requirements 2.4**

- [ ]* 3.6 Write unit tests for authentication routes
  - Test duplicate email registration rejection
  - Test session persistence across requests
  - Test redirect behavior after login/logout
  - _Requirements: 1.3, 2.3, 2.4_

- [ ] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement dashboard route and template
  - Create src/routes/main.py blueprint
  - Implement GET / route with login_required decorator
  - Query all facts with their categories and creators
  - Create src/templates/base.html with common layout structure
  - Create src/templates/dashboard.html with application explanation and fact list
  - Display fact titles, categories, and navigation options
  - Handle empty state when no facts exist
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ]* 5.1 Write property test for dashboard displays all facts
  - **Property 7: Dashboard displays all facts**
  - **Validates: Requirements 3.2**

- [ ]* 5.2 Write unit tests for dashboard
  - Test dashboard requires authentication
  - Test empty state display
  - Test navigation elements presence
  - _Requirements: 3.3, 3.4_

- [ ] 6. Implement category management
  - Implement GET /category/new route with category creation form
  - Implement POST /category/new route with validation and category creation
  - Create src/templates/category_form.html with semantic HTML and CSS classes
  - Validate category name is not empty or whitespace-only
  - Handle duplicate category name errors
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 6.1 Write property test for category creation
  - **Property 12: Category creation with valid name**
  - **Validates: Requirements 5.1**

- [ ]* 6.2 Write property test for empty category name rejection
  - **Property 13: Empty category name rejection**
  - **Validates: Requirements 5.3**

- [ ]* 6.3 Write unit tests for category management
  - Test duplicate category name rejection
  - Test category appears in fact creation form
  - _Requirements: 5.2, 5.4_

- [ ] 7. Implement fact creation
  - Implement GET /fact/new route with fact creation form
  - Implement POST /fact/new route with validation and fact creation
  - Create src/templates/fact_form.html with semantic HTML and CSS classes
  - Load all categories for dropdown selection
  - Validate fact title is not empty or whitespace-only
  - Store creator user ID and creation timestamp
  - Redirect to dashboard after successful creation
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ]* 7.1 Write property test for fact creation with valid data
  - **Property 8: Fact creation with valid data**
  - **Validates: Requirements 4.1, 4.4**

- [ ]* 7.2 Write property test for empty title rejection
  - **Property 9: Empty title rejection**
  - **Validates: Requirements 4.2**

- [ ]* 7.3 Write property test for created facts appear on dashboard
  - **Property 10: Created facts appear on dashboard**
  - **Validates: Requirements 4.3**

- [ ]* 7.4 Write property test for categories available for fact creation
  - **Property 14: Categories available for fact creation**
  - **Validates: Requirements 5.4**

- [ ] 8. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement fact viewing and evaluation
  - Implement GET /fact/<id> route to display fact details
  - Query fact with category, creator, and all evaluations
  - Calculate evaluation counts (true vs false)
  - Create src/templates/fact_detail.html with fact information display
  - Display Fact and Fake buttons
  - Display input field for supporting info
  - Display all previous evaluations with counts
  - Display supporting info for each evaluation
  - _Requirements: 6.1, 6.5, 7.1, 7.4_

- [ ]* 9.1 Write property test for fact details display
  - **Property 11: Fact details display completely**
  - **Validates: Requirements 6.1**

- [ ]* 9.2 Write property test for evaluation display with counts
  - **Property 17: Evaluation display with counts**
  - **Validates: Requirements 6.5**

- [ ]* 9.3 Write property test for supporting info display
  - **Property 18: Supporting info display**
  - **Validates: Requirements 7.4**

- [ ]* 9.4 Write unit tests for fact viewing
  - Test fact detail page requires authentication
  - Test 404 for non-existent fact
  - Test supporting info input field presence
  - _Requirements: 7.1_

- [ ] 10. Implement evaluation submission
  - Implement POST /fact/<id>/evaluate route
  - Accept is_true boolean parameter (true for Fact, false for Fake)
  - Accept optional supporting_info parameter
  - Create Evaluation record with user ID and timestamp
  - Store supporting info if provided
  - Redirect back to fact detail page
  - _Requirements: 6.2, 6.3, 6.4, 7.2, 7.3_

- [ ]* 10.1 Write property test for evaluation recording with metadata
  - **Property 15: Evaluation recording with metadata**
  - **Validates: Requirements 6.2, 6.3, 6.4**

- [ ]* 10.2 Write property test for supporting info storage
  - **Property 16: Supporting info storage**
  - **Validates: Requirements 7.2, 7.3**

- [ ]* 10.3 Write unit tests for evaluation submission
  - Test evaluation requires authentication
  - Test evaluation for non-existent fact returns 404
  - Test multiple evaluations by same user
  - _Requirements: 6.2, 6.3_

- [ ] 11. Implement base CSS stylesheet
  - Create src/static/css/main.css with CSS custom properties
  - Define color scheme, typography, and spacing variables
  - Implement BEM-style classes for layout components (container, header, main, footer)
  - Implement BEM-style classes for form components (form, form__group, form__label, form__input)
  - Implement BEM-style classes for button components (button, button--primary, button--secondary)
  - Implement BEM-style classes for card components (card, card__title, card__content)
  - Implement BEM-style classes for dashboard (dashboard, dashboard__header, dashboard__facts)
  - Implement BEM-style classes for fact detail (fact-detail, fact-detail__info, fact-detail__evaluations)
  - Ensure all styles use semantic class names
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 12. Implement error handling
  - Add error handlers for 400, 401, 403, 404, 500 status codes
  - Create error templates with consistent styling
  - Implement flash messages for user feedback
  - Add try-except blocks for database operations
  - Implement validation error messages in forms
  - Configure logging for production errors
  - _Requirements: 1.2, 1.3, 2.2, 4.2, 5.2, 5.3_

- [ ]* 12.1 Write unit tests for error handling
  - Test 404 error page
  - Test validation error messages
  - Test database error handling
  - _Requirements: 1.2, 4.2, 5.3_

- [ ] 13. Configure application for development and production
  - Set up environment variable loading
  - Configure Flask app with development settings (DEBUG=True, SQLite)
  - Configure Flask app with production settings (DEBUG=False, PostgreSQL)
  - Set up database initialization script
  - Create run script for development server (127.0.0.1:5001)
  - Create Gunicorn configuration for production
  - Add database migration support with Flask-Migrate
  - _Requirements: All_

- [ ] 14. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ]* 15. Write integration tests
  - Test complete registration and login flow
  - Test creating category, then creating fact in that category
  - Test creating fact, then evaluating it with supporting info
  - Test creating fact, then evaluating it without supporting info
  - Test viewing dashboard after creating multiple facts
  - _Requirements: All_
