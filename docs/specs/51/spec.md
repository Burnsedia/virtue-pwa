# Spec: Backend Tests for Account Creation & Auth — Issue #51 (merged with #56)

- **Status:** Draft (AI) — awaiting your edit
- **Owner:** AI (grunt) — you review the PR
- **Branch:** `feat/51-backend-auth-tests` (create after #52 merges)
- **Blocked by:** #52 (Djoser refactor)
- **Priority:** P0 — proves the foundation

## Background
`backend/core/api/tests.py` is 652 lines covering Profile/Organization/Project/Issue/TimeLog/Report models and their APIs — but **zero coverage of users, account creation, JWT, or Djoser endpoints**. This issue closes that gap, test-first against the #52 spec.

## Current behavior (grounded facts)
- Existing test classes: `ProfileModelTest`, `OrganizationModelTest`, `ProjectModelTest`, `IssueModelTest`, `TimeLogModelTest`, `OrganizationAPITest`, `ProjectAPITest`, `IssueAPITest`, `TimeLogAPITest`, `ProjectReportAPITest` (+ more below line 554).
- No tests touch `/auth/` endpoints or the `User` model directly.

## Test cases to write (follow existing patterns)
**Account creation — `POST /auth/users/`**
1. Creates user with username/email/password → 201, user exists in DB, password hashed (not plaintext).
2. Duplicate username → 400.
3. Duplicate email → 400.
4. Missing password → 400.
5. Weak password (fails MinimumLengthValidator) → 400.
6. `Profile` created automatically via signal after user creation.

**JWT — `/auth/jwt/`**
7. `create` with valid creds → 200, returns `access` and `refresh`.
8. `create` with wrong password → 401.
9. `refresh` with valid refresh token → 200, new access.
10. `refresh` with garbage token → 401.

**Authenticated endpoints**
11. `GET /auth/users/me/` with valid token → 200, correct user.
12. `GET /auth/users/me/` without token → 401 (or 403 — assert what DRF actually returns).
13. `GET /api/users/me/subscription_status/` authed free user → `{"is_premium": false}`.
14. (If premium path kept) subscription status for premium user — mock `djstripe` Customer/Subscription.

**Logout** (if endpoint exists after #52)
15. Stateless logout returns expected status (205 or 200 per chosen design).

**Regression guards (from the backend audit)**
16. `settings.DJOSER["SERIALIZERS"]["user_create"]` resolves via `import_string` — catches the missing-module class of bug that broke signup.
17. `POST /auth/jwt/verify/` with valid token → 200; tampered token → 401.
18. Expired/forged access token against a protected endpoint (`/api/organizations/`) → 401.
19. `POST /auth/users/set_password/` with correct `current_password` → old password stops working, new one logs in; wrong `current_password` → 400.

**Fix the likely-broken existing test**
20. `tests.py:62` `test_organization_with_members` asserts owner auto-added to `members` — no model logic does this. Fix the behavior (in #52) or the assertion (here), whichever the spec owner decides.

## In scope
- `backend/core/api/tests.py` (extend) or new `backend/core/api/test_auth.py` — your preference; suggest separate `test_auth.py` file for clarity.

## Out of scope
- Changing auth behavior itself (that's #52), frontend tests (#50), e2e (#93).

## Acceptance criteria
- [ ] `python manage.py test` green, including the new auth tests.
- [ ] Coverage of the auth surface above (aim ≥15 new tests).
- [ ] Tests assert against the #52 spec's acceptance criteria (real behavior, not assumptions).

## Risks
- Djoser version quirks (2.3.1) — assert actual response shapes, don't invent them.
- `djstripe` Customer queries in `is_user_premium` may need mocking to avoid Stripe calls.

## Open questions
1. New file (`test_auth.py`) or extend `tests.py`?
2. Premium-case test in scope for the weekend, or free-user only?
