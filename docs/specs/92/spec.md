# Spec: Refactor SignUp Page Frontend — Issue #92

- **Status:** Draft (AI) — awaiting your edit
- **Owner:** Split (see Open Questions)
- **Branch:** `feat/92-signup-refactor` (create after #53 merges)
- **Blocked by:** #53 (nano stores)
- **Blocks:** #93 (e2e)
- **Priority:** P1

## Background
The signup flow works against Djoser but is built the same sloppy way as login: hardcoded URLs, `alert()` errors, unvalidated UX. Bring it to the same standard as #49, using the #53 stores.

## Current behavior (grounded facts)
- `frontend/src/pages/signup.astro` (10 lines) renders `SignupForm.vue` — this page is the canonical signup. (`register.astro` is empty; deleted in #49.)
- `SignupForm.vue` (82 lines): Options API; fields email/username/password/confirmPassword; hardcoded `http://localhost:8000/auth/users/`; client-side password match check via `alert()`; on success: `alert('Registration successful!')` + redirect `/signin`; on failure: `alert(JSON.stringify(errorData))` — raw Djoser error payload dumped at the user.
- Backend (`DJOSER`): `USER_CREATE_PASSWORD_RETYPE: False`, `LOGIN_FIELD: username`, `SEND_ACTIVATION_EMAIL: False` — so `confirmPassword` is client-only, and activation emails are off.

## Goals
1. **Refactor `SignupForm.vue`**: env-based API URL (match #49), inline error UI, loading state, remove alerts.
2. **Map Djoser errors to friendly messages**: `username already exists`, `email already exists`, weak password → human-readable field errors (Djoser returns field-keyed dicts).
3. **Success flow decision**: either (a) redirect to `/signin` with a "account created, sign in" notice, or (b) auto-login (call JWT create with the new creds and set stores). Your call — (b) is nicer UX but couples to #52/#53 state.
4. Client validation: password match inline (not alert), min length hint matching Django validators.
5. Update cross-links: AuthForm links to `/signup` (keep if canonical); ensure header link consistent with #49 outcome.

## In scope
- `components/SignupForm.vue`, `pages/signup.astro` (if changes needed), links from `AuthForm.vue`/header (coordinate with #49).

## Out of scope
- Backend user-create behavior (#52), stores (#53), login page (#49), tests (#50 covers login; signup tests: see Test plan).

## Acceptance criteria
- [ ] `npm run build` passes.
- [ ] Signup success reaches the chosen flow (redirect or auto-login) with no `alert()`.
- [ ] Field-level error messages shown inline for duplicate username/email, weak password.
- [ ] No hardcoded `localhost:8000`.
- [ ] Password mismatch shows inline before any request.

## Test plan
- Component tests for SignupForm (mismatch, success, error mapping) — add alongside #50 or in #50's PR (your call on placement).

## Risks
- Auto-login option depends on JWT shape from #52 — coordinate.
- Djoser error dict shapes vary by field — assert against real responses (see #51 tests).

## Open questions (your call)
1. Success flow: redirect-to-signin or auto-login?
2. Do you write SignupForm yourself, or AI drafts and you polish?
3. Should signup tests live in this issue or #50?

## Audit addendum (Ornith 35B frontend audit)
- Add `autocomplete` attributes (`email`, `username`, `new-password`) and proper label↔input association (finding 3.2).
- Consider a shared fieldset component for username/password fields used by both `AuthForm` and `SignupForm` (near-identical blocks) — only if it doesn't slow the weekend.
- Error display should use the same accessible toast as #49 (finding 3.3) — coordinate implementation order.
- `SignupForm` sends no `re_password` while backend has `USER_CREATE_PASSWORD_RETYPE: False` — consistent, but confirm this stays aligned after #52 decisions.
- On success the audit suggests redirect to `/signin` (simpler); auto-login remains the nicer-UX option — your call unchanged.
