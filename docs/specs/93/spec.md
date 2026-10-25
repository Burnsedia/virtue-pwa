# Spec: E2E Tests for Auth Flow — Issue #93

- **Status:** Draft (AI) — awaiting your edit
- **Owner:** AI (grunt) — you review the PR
- **Branch:** `feat/93-auth-e2e` (create after #49 + #92 + #51 merge)
- **Blocked by:** #49, #92, #51
- **Priority:** P1 — **weekend stretch goal** (spills to Monday if it fights back)

## Background
No e2e tooling exists in the repo. This issue adds Playwright (or Cypher—your call) and covers the full auth journey end-to-end: signup → login → protected page → logout.

## Current behavior (grounded facts)
- `frontend/package.json` has **no e2e runner** (no Playwright, no Cypress).
- Auth flow spans: Astro pages (`/signup`, `/signin` or `/login`), Vue components (AuthForm, SignupForm), nano stores, Django backend (`/auth/*`).
- Backend runs via `python manage.py runserver` (port 8000); frontend via `npm run dev` (port 4321).

## Scope
1. **Install & configure Playwright** (`@playwright/test` + chromium only to keep the weekend light). Add `test:e2e` script. Add `webServer` config to auto-start backend + frontend (or document manual steps — your call).
2. **Scenarios** (happy path first, then negative):
   - Signup: new user → success → lands on signin (or auto-login per #92).
   - Duplicate signup: error message visible, no crash.
   - Login: valid creds → home, header shows logged-in state.
   - Login: bad password → inline error visible.
   - Protected page: unauthenticated visit → redirected to signin (if route guards landed in #49; otherwise assert 401 handling).
   - Logout: header → logged-out state, protected page blocked again.
3. **Test data isolation**: create unique usernames per run (timestamp suffix) against the local SQLite dev DB; document DB reset command.

## In scope
- `frontend/playwright.config.ts`, `frontend/e2e/auth.spec.ts` (or `tests/e2e/`), package.json scripts, docs note in this spec.

## Out of scope
- Unit/vitest tests (#50), non-auth e2e (projects/issues flows — future).

## Acceptance criteria
- [ ] `npm run test:e2e` runs green locally with backend + frontend up.
- [ ] All scenarios above pass.
- [ ] No flaky waits — use locators + auto-retry, not `sleep()`.

## Risks
- **Highest-risk issue of the weekend.** Playwright install + Astro islands hydration timing = classic flake source. If it slips, cut scenarios, not quality.
- Backend DB state pollution — isolate with unique usernames and a reset script.
- Chrome/chromium download size on your box (Arc B70 — fine, just time).

## Open questions (your call)
1. Playwright or Cypress? (I recommend Playwright — better with Astro.)
2. Auto-start both servers in config, or manual start + documented script?
3. If time runs out: drop this to Monday or cut to happy-path-only?
