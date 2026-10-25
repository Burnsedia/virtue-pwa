# Spec: Refactor Django Djoser Auth — Issue #52

- **Status:** Draft (AI) — awaiting your edit
- **Owner:** You (core refactor) + AI (tests in #51, review)
- **Branch:** `feat/52-djoser-refactor` (created)
- **Blocks:** #51 (backend tests)
- **Priority:** P0 — foundation

## Background
The auth backend is half-broken AI-generated code. Djoser is installed but misconfigured, and at least two runtime breakages exist today. Goal: working, default-style Djoser + SimpleJWT auth that the rest of the epic builds on.

## Current behavior (grounded facts)
- `DJOSER` in `backend/core/core/settings.py` references `api.djoser_serializers.UserCreateSerializer` — **file does not exist** → ImportError on any auth call.
- `UserSubscriptionStatusView` exists in `views.py` but its URL (`users/me/subscription_status/`) is **commented out** in `api/urls.py` — yet the frontend calls it on every login → login flow 404s.
- No `SIMPLE_JWT` settings block → default token lifetimes (access 5 min, refresh 1 day), no rotation config.
- `SECRET_KEY` hardcoded insecure; `DEBUG=True`; `CORS_ALLOW_ALL_ORIGINS=True`; `ALLOWED_HOSTS=[]`.
- `requirments.txt` (typo'd filename) is missing `djstripe` and `stripe` despite both being imported in `views.py`.
- `from .serializers import *` / `from .views import *` star imports in `views.py` / `urls.py`.
- social-auth packages installed but unused (slop).
- `signals.py` creates a bare `Profile` per user — fine, keep.

## Weak spots to fix
1. **Create `backend/core/api/djoser_serializers.py`** with `UserCreateSerializer` (username + email + password, password write-only). Match `LOGIN_FIELD: "username"`.
2. **Wire the subscription status endpoint** (uncomment + register in `api/urls.py`) — or decide to drop it and change the frontend instead (see Open Questions).
3. **Add `SIMPLE_JWT` settings**: explicit lifetimes (e.g., access 60 min, refresh 7 days), refresh token reuse policy. **Include an explicit `SIGNING_KEY` decoupled from `SECRET_KEY`** — today the committed insecure `SECRET_KEY` is the JWT signing key, meaning anyone with repo access can forge valid JWTs for any user.
4. **Env-driven settings**: move `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` to environment vars (e.g., `os.environ.get` or django-environ) with sane dev defaults. Provide `.env.example`.
5. **Fix requirements file**: rename to `requirements.txt`, add `djstripe` and `stripe` (or remove djstripe if you want Stripe out of scope — see Open Questions). Also drop unused social-auth deps (`oauthlib`, `python3-openid`, `requests-oauthlib`, `social-auth-app-django`, `social-auth-core`) — no config anywhere references them.
6. **Replace star imports** with explicit imports.
7. **Harden serializers** (`api/serializers.py`): all seven use `fields = '__all__'` with no `read_only_fields` — `owner`/`user_owner`/`org_owner`/`user` FKs are client-writable via PATCH/PUT (ownership-reassignment/IDOR vector). Add `read_only_fields`.
8. **Consistency**: `TimeLogViewSet` omits `permission_classes` that every sibling declares (relies on global default) — make it explicit.
9. **Consider throttle classes** on `/auth/jwt/create/` and `/auth/users/` (DRF throttling) — brute-force surface with none today.

## Audit addendum (DeepSeek V4 Pro backend audit)
- Signup is **hard-broken today**: `POST /auth/users/` → `ImportError` → 500.
- `stripe.api_key = settings.STRIPE_SECRET_KEY` runs at import time in `views.py` with a placeholder value.
- `is_user_premium` requires a dj-stripe Customer/Subscription, so the "5 free projects" cap in `ProjectViewSet.create` always applies on a fresh DB; `IsPremiumUser` is never applied to any view.
- `api/signals.py:16` `save_user_profile` calls `instance.profile.save()` on every user save → `RelatedObjectDoesNotExist` risk for users without a Profile (bulk_create, createsuperuser races).
- `api/urls.py:12-21` contains a large commented-out block with an in-code note "these are AI gen and I do not trust these api end points" — decide: delete or re-enable.
- `tests.py:62` (`test_organization_with_members`) asserts the owner is auto-added to `members` — but no model/signal logic does that. **Likely a failing/false test; fix the test or the behavior in #52/#51.**

## In scope
- Files: `core/settings.py`, `core/urls.py`, `api/urls.py`, `api/djoser_serializers.py` (new), `api/views.py`, `requirments.txt`
- Endpoints that must work: `POST /auth/jwt/create/`, `POST /auth/jwt/refresh/`, `POST /auth/users/`, `GET /auth/users/me/`, `POST /auth/token/logout/` (or your chosen logout), subscription status (decision pending).

## Out of scope
- Stripe checkout/portal endpoints (already commented out), social auth (unless you want it deleted), frontend changes (that's #49/#53/#92).

## Acceptance criteria
- [ ] `python manage.py check` passes; server boots with no ImportError.
- [ ] `POST /auth/users/` creates a user (username/email/password); duplicate username rejected with 400.
- [ ] `POST /auth/jwt/create/` returns access + refresh for valid creds; 401 for bad creds.
- [ ] `POST /auth/jwt/refresh/` returns new access.
- [ ] `GET /auth/users/me/` returns the user with a valid token; 401 without.
- [ ] `GET /api/users/me/subscription_status/` returns `{"is_premium": false}` for authed free user (or endpoint intentionally removed + frontend updated).
- [ ] No secrets in code; `.env.example` documented.
- [ ] Backend test suite green (existing 652-line suite + new #51 tests).

## Test plan (test-first, implemented in #51)
Tests are written by AI **after** this refactor lands (Wave 2). They will assert: user creation happy/duplicate/missing-field/weak-password, JWT create/refresh/401, users/me auth, subscription status, Profile signal. See `docs/specs/51/spec.md`.

## Risks
- Djoser + custom `UserCreateSerializer` interplay (re-validation quirks) — keep it thin.
- Renaming `requirments.txt` may break other scripts — check references first.
- `djstripe` requires syncing Stripe models (`python manage.py djstripe_sync_models`) — if painful, strip djstripe now (check `permissions.py` dependency).

## Open questions (your call)
1. Keep `LOGIN_FIELD: username` or switch to email? (Frontend currently sends username.)
2. Keep `users/me/subscription_status/` or drop it and simplify the frontend login flow?
3. djstripe: keep (add to requirements) or remove (drop from INSTALLED_APPS, permissions, views)?
4. Logout: SimpleJWT stateless logout (client discards token) or token blacklist app?
5. Token lifetimes you want?
