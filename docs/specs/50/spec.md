# Spec: Vitest Tests for Login — Issue #50

- **Status:** Draft (AI) — awaiting your edit
- **Owner:** AI (grunt) — you review the PR
- **Branch:** `feat/50-login-vitest` (create after #49 merges)
- **Blocked by:** #49 (login refactor), #53 (stores)
- **Priority:** P1

## Background
Frontend has Vitest + Vue Test Utils + jsdom configured with 3 test files (IssueCard, PomodoroTimer, utils) and a `setup.ts` mocking localStorage. Nothing covers auth. This issue tests the new login flow and stores, test-first where possible.

## Current behavior (grounded facts)
- `frontend/package.json`: `vitest ^4.1.11`, `@vue/test-utils ^2.5.0`, `jsdom ^23.0.1`, scripts `test`/`test:ui`/`test:run`.
- `frontend/src/test/setup.ts` mocks `localStorage` globally.
- Existing tests: `components/__tests__/IssueCard.test.ts`, `PomodoroTimer.test.ts`, `test/utils.test.ts`.

## Test cases to write
**authStore (`frontend/src/lib/stores/`)**
1. `login()` sets `$token`, `$refreshToken`, `$user`, `$isPremium`; values persisted (localStorage mock).
2. `logout()` clears all atoms.
3. `isLoggedIn` derived store: false initially, true after login, false after logout.
4. `getAuthHeaders()` returns Bearer header when logged in, empty/undefined when not.
5. SSR guard: importing the store without `window` doesn't crash (jsdom has window — test persistence init path instead, or use `vi.stubEnv`).

**AuthForm.vue (after #49 refactor)**
6. Renders username/password fields + submit.
7. Successful submit: fetch mocked → store login called with access+refresh+user → router/navigation called.
8. Failed submit (401): inline error message rendered, no alert, store untouched.
9. Loading state: button disabled while request in flight.
10. No token values logged to console (spy on console.log).

**SignupForm.vue (if placed here, see #92 Open Questions)**
11. Password mismatch shows inline error, no request made.
12. Duplicate username response → field error mapped and shown.
13. Success → redirect/auto-login per #92 decision.

## In scope
- `frontend/src/lib/stores/__tests__/authStore.test.ts`, `frontend/src/components/__tests__/AuthForm.test.ts` (+ SignupForm if agreed).

## Out of scope
- Backend tests (#51), e2e (#93), new features.

## Acceptance criteria
- [ ] `npm run test:run` green including new suites.
- [ ] Every public auth-store action/derivation covered.
- [ ] AuthForm core paths covered (success, failure, loading).
- [ ] No test depends on real network (fetch fully mocked).

## Risks
- jsdom localStorage mock may need persistence events — check `@nanostores/persistent` behavior under jsdom.
- Vue Router navigation assertions — if no router in tests, assert on `window.location.assign` spy or mock.

## Open questions
1. Include SignupForm tests here or under #92?
2. Coverage threshold target (e.g., ≥80% on auth files)?

## Audit addendum (Ornith 35B frontend audit)
- **`setup.ts` traps**: global `localStorage.getItem` mock returns `undefined` (audit 6.2), and global `fetch` is `vi.fn()` returning `undefined` — so `res.ok` throws in any unmocked test. **Fix `setup.ts` first**: provide an in-memory localStorage implementation; keep fetch mocked but reset in `beforeEach` (follow `PomodoroTimer.test.ts` per-test mocking style).
- Add a store-integration test: a consumer component (`PricingPage` or `OrganizationList`) re-renders its gated section reactively when the auth store updates — proves the #53 reactivity fix end-to-end (audit 6.1).
- Assert **no `console.log`** in the happy path (token-leak regression guard, audit 4.2) and **no `window.alert`** usage (audit 3.3).
