# Security Review - Book Sharing Application

**Review Date:** December 1, 2025  
**Reviewed Against:** [Amazon Q Detector Library for Python](https://docs.aws.amazon.com/codeguru/detector-library/python/)  
**Severity Levels:** Critical, High

---

## Executive Summary

This security review identified **3 Critical** and **4 High** severity findings in the Book Sharing Application codebase. The findings primarily relate to hardcoded credentials, insecure configuration, CSRF protection gaps, and improper input validation.

---

## Critical Findings

### 1. Hardcoded Credentials (CRITICAL)
**Detector ID:** `python/hardcoded-credentials@v1.0`  
**CWE:** [CWE-798](https://cwe.mitre.org/data/definitions/798.html)  
**Category:** Security

**Location:** `.env` file (line 2)

**Description:**  
The application contains hardcoded credentials in the `.env` file that is committed to version control. The `SECRET_KEY` is set to `dev_secret_key_replace_in_production`, which is a weak, predictable value.

**Code:**
```python
# .env
SECRET_KEY=dev_secret_key_replace_in_production
```

**Impact:**  
- Session hijacking and forgery attacks
- CSRF token prediction
- Credential exposure through version control history
- Compromise of all session-based security mechanisms

**Recommendation:**
1. Remove `.env` from version control (add to `.gitignore`)
2. Generate strong random secrets using `secrets.token_hex(32)`
3. Store secrets in environment variables or secure secret management systems
4. Rotate all existing secrets immediately

**Compliant Example:**
```python
# Use environment variables
SECRET_KEY=os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")
```

---

### 2. Insecure Cookie Configuration (CRITICAL)
**Detector ID:** `python/insecure-cookie@v1.0`  
**CWE:** [CWE-614](https://cwe.mitre.org/data/definitions/614.html)  
**Category:** Security

**Location:** `src/app.py` (application configuration)

**Description:**  
The application does not configure secure cookie settings for session management. Missing `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, and `SESSION_COOKIE_SAMESITE` flags expose sessions to interception and CSRF attacks.

**Current Code:**
```python
# src/app.py (lines 23-27)
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
```

**Impact:**
- Session cookies transmitted over unencrypted HTTP connections
- JavaScript access to session cookies (XSS vulnerability amplification)
- Cross-site request forgery attacks
- Session hijacking through man-in-the-middle attacks

**Recommendation:**
Add secure cookie configuration:

```python
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_SECURE=True,  # Only send over HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',  # CSRF protection
)
```

---

### 3. Enabling Debug Feature in Production (CRITICAL)
**Detector ID:** `python/detect-activated-debug-feature@v1.0`  
**CWE:** [CWE-489](https://cwe.mitre.org/data/definitions/489.html)  
**Category:** Security

**Location:** `src/app.py` (line 80), `run.py` (line 16)

**Description:**  
Debug mode code is present and commented out but easily enabled. Debug mode exposes sensitive information including stack traces, source code, and environment variables.

**Code:**
```python
# src/app.py (line 80)
#app.run(debug=True)

# run.py (line 16)
# app.run(debug=True, port=5000)
```

**Impact:**
- Exposure of application source code and file paths
- Detailed stack traces revealing internal logic
- Interactive debugger accessible to attackers
- Information disclosure enabling targeted attacks

**Recommendation:**
1. Remove all hardcoded `debug=True` statements
2. Use environment variables exclusively for debug control
3. Ensure production deployments never enable debug mode

**Compliant Example:**
```python
# Only use environment variable control
debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
if os.environ.get('FLASK_ENV') == 'production' and debug_mode:
    raise ValueError("Debug mode cannot be enabled in production")
app.run(debug=debug_mode, port=5000)
```

---

## High Severity Findings

### 4. Cross-Site Request Forgery (CSRF) Protection Bypass (HIGH)
**Detector ID:** `python/cross-site-request-forgery@v1.0`  
**CWE:** [CWE-352](https://cwe.mitre.org/data/definitions/352.html)  
**Category:** Security

**Location:** `src/routes/books.py` (line 148)

**Description:**  
The `toggle_visibility` endpoint explicitly disables CSRF protection using `@csrf.exempt`, allowing attackers to forge requests that modify book visibility.

**Code:**
```python
@books_bp.route('/<int:book_id>/toggle-visibility', methods=['POST'])
@login_required
@csrf.exempt  # SECURITY ISSUE
def toggle_visibility(book_id):
    book = Book.query.get_or_404(book_id)
    # ... toggle logic
```

**Impact:**
- Attackers can force users to hide/show books without consent
- State-changing operations vulnerable to CSRF attacks
- Potential for automated attacks against authenticated users

**Recommendation:**
Remove the `@csrf.exempt` decorator and ensure CSRF tokens are included in all forms:

```python
@books_bp.route('/<int:book_id>/toggle-visibility', methods=['POST'])
@login_required
# Remove @csrf.exempt
def toggle_visibility(book_id):
    # CSRF protection automatically enforced
    book = Book.query.get_or_404(book_id)
    # ... rest of logic
```

---

### 5. URL Redirection to Untrusted Site (HIGH)
**Detector ID:** `python/open-redirect@v1.0`  
**CWE:** [CWE-601](https://cwe.mitre.org/data/definitions/601.html)  
**Category:** Security

**Location:** `src/routes/auth.py` (lines 88-93)

**Description:**  
The login function accepts a `next` parameter from user input and redirects to it after authentication. While there is basic validation, it only checks if the path starts with `/`, which is insufficient to prevent open redirect attacks.

**Code:**
```python
# src/routes/auth.py (lines 88-93)
next_page = request.args.get('next')
if next_page:
    # Validate that next_page is a relative path
    if not next_page.startswith('/'):
        next_page = '/'
    return redirect(next_page)
```

**Impact:**
- Phishing attacks using trusted domain in redirect chain
- Credential theft through lookalike domains
- Malware distribution via trusted redirect

**Recommendation:**
Use Flask's `url_for()` with safe URL validation:

```python
from urllib.parse import urlparse, urljoin
from flask import request

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

next_page = request.args.get('next')
if next_page and is_safe_url(next_page):
    return redirect(next_page)
return redirect(url_for('main.index'))
```

---

### 6. Improper Input Validation (HIGH)
**Detector ID:** `python/improper-input-validation@v1.0`  
**CWE:** [CWE-20](https://cwe.mitre.org/data/definitions/20.html)  
**Category:** Security

**Location:** `src/routes/books.py` (multiple endpoints)

**Description:**  
User-provided book IDs and request IDs are used directly in database queries without proper validation beyond type conversion. While SQLAlchemy provides some protection, additional validation is needed.

**Code Examples:**
```python
# src/routes/books.py
@books_bp.route('/<int:book_id>')
def view(book_id):
    book = Book.query.get_or_404(book_id)  # Minimal validation
    # ...
```

**Impact:**
- Potential for enumeration attacks
- Information disclosure through error messages
- Unauthorized access to resources

**Recommendation:**
Add explicit validation and authorization checks:

```python
@books_bp.route('/<int:book_id>')
@login_required
def view(book_id):
    if book_id <= 0:
        abort(400, "Invalid book ID")
    
    book = Book.query.get_or_404(book_id)
    
    # Check authorization for hidden books
    if book.is_hidden and book.owner_id != current_user.user_id:
        abort(404)
    
    # ... rest of logic
```

---

### 7. Missing Authorization Checks (HIGH)
**Detector ID:** `python/missing-authorization@v1.0`  
**CWE:** [CWE-862](https://cwe.mitre.org/data/definitions/862.html)  
**Category:** Security

**Location:** `src/routes/books.py` (line 35)

**Description:**  
The `view` endpoint for books requires authentication but doesn't verify if the user should have access to hidden books. A user can potentially view hidden books by directly accessing the URL.

**Code:**
```python
@books_bp.route('/<int:book_id>')
@login_required  # Only checks authentication, not authorization
def view(book_id):
    book = Book.query.get_or_404(book_id)
    # No check if book is hidden and user is not the owner
```

**Impact:**
- Unauthorized access to private/hidden books
- Information disclosure
- Privacy violation

**Recommendation:**
Add authorization check for hidden books:

```python
@books_bp.route('/<int:book_id>')
@login_required
def view(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Authorization check for hidden books
    if book.is_hidden and book.owner_id != current_user.user_id:
        abort(403, "You don't have permission to view this book")
    
    # ... rest of logic
```

---

## Summary of Findings

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 3 | Hardcoded Credentials, Insecure Cookies, Debug Mode |
| High | 4 | CSRF Bypass, Open Redirect, Input Validation, Missing Authorization |
| **Total** | **7** | |

---

## Remediation Priority

1. **Immediate (Critical):**
   - Remove hardcoded credentials from `.env` and version control
   - Configure secure cookie settings
   - Remove debug mode code

2. **High Priority (High):**
   - Remove CSRF exemption from toggle_visibility
   - Fix open redirect vulnerability in login
   - Add authorization checks for hidden books
   - Implement comprehensive input validation

3. **Follow-up Actions:**
   - Conduct security training for development team
   - Implement automated security scanning in CI/CD pipeline
   - Perform penetration testing after fixes
   - Review and update security policies

---

## References

- [Amazon Q Detector Library - Python](https://docs.aws.amazon.com/codeguru/detector-library/python/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)
