# secure-coding-review-flask
Secure coding review of a Flask app — 8 vulnerabilities identified via static analysis (Bandit) and manual review, each documented with CWE mapping, impact, and a remediated fix.
# Secure Coding Review — Flask Notes App

A hands-on secure coding review project: a small intentionally-vulnerable Flask
application (`app_vulnerable.py`) was built as an audit target, then reviewed using
both static analysis (Bandit) and manual code inspection to identify security
vulnerabilities. Each finding is documented with severity, CWE mapping, impact,
and remediation, and a fully patched version (`app_fixed.py`) is included.

## What's in this repo

- `app_vulnerable.py` — sample app with 8 deliberately introduced vulnerabilities
- `app_fixed.py` — remediated version, each fix labeled to match the report
- `bandit_report.txt` — raw static analyzer output
- `security_review_report.docx` — full write-up: methodology, findings table,
  detailed analysis per vulnerability, and general secure coding recommendations

## Vulnerabilities covered

SQL injection, hardcoded secrets, plaintext password storage, stored XSS,
OS command injection, path traversal, debug mode exposure, and insecure
network binding — mapped to their CWE IDs.

## Key takeaway

Bandit's static analysis caught 6 of the 8 issues automatically. The stored XSS
and path traversal vulnerabilities were only found through manual review, since
static tools don't trace how a variable is used once it reaches an HTML string
or file path. This project was built to demonstrate that a real security review
needs both approaches.

## Tools used

Python, Flask, SQLite, Bandit

---
*Built with AI assistance (Claude) for the vulnerable/fixed app code and report
generation; vulnerability analysis and remediation choices were reviewed and
verified by me.*
