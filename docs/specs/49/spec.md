# Spec: Refactor Login Page — Remove AI Slop & Deduplicate — Issue #49

- **Status:** Draft (AI) — awaiting your edit
- **Owner:** Split (see Open Questions) — component logic possibly yours, cleanup grunt AI's
- **Branch:** `feat/49-login-refactor` (create after #53 merges)
- **Blocked by:** #53 (nano stores)
- **Blocks:** #50 (vitest login), #93 (e2e)
- **Priority:** P1

## Background
Login exists twice and works once. Clean it up into a single, modern Vue 3 login flow backed by the #53 nano stores, with real error handling instead of `alert()`.

## Current behavior (grounded facts)
- `frontend/src/pages/login.astro`: 9-line empty shell ("Welcome to Astro.") — **dead page**.
- `frontend/src/pages/signin.astro`: real page rendering `AuthForm.vue` (`client:load`, `:isLogin="true"`).
- `frontend/src/pages/register.astro`: **0 bytes, empty file** — dead page.
- `AuthForm.vue` (93 lines): Options API; hardcoded `http://localhost:8000` (×3); stores only `data.access` (refresh token **discarded**); calls `/api/users/me/subscription_status/` which is 404 on the backend (endpoint commented out) → login flow throws even on correct credentials; `alert()` for success and errors; `console.log` token values; `window.location.assign('/')` navigation.
- `header.astro` always shows "Sign In"/"Sign Up" links — no logged-in state, no logout.
- Route convention: `/signin` is referenced across the app (header, AuthForm link to `/signup`).

## Goals
1. **One login route.** Decide canonical (`/signin` or `/login`). Delete the dead one. Redirect the old path to the new one if you keep compat.
2. Delete empty `register.astro`.
3. **Refactor `AuthForm.vue`**: `<script setup>` (or keep Options — your call), API base URL from env (`import.meta.env.PUBLIC_API_URL` with `http://localhost:8000` fallback or Vite proxy), store **both** access + refresh via auth store actions from #53, inline error message UI (no `alert`), loading state on button, remove console.logs of tokens.
4. **Subscription status**: align with #52 decision — call the (now working) endpoint via the store, or drop the call entirely.
5. **Header**: consume `$user`/`isLoggedIn` store — show Sign In/Up when logged out; show user + Logout button when logged in. (Needs a client-side island component, e.g., `AuthNav.vue` inside `header.astro`.)
6. Route guard consideration: redirect unauthenticated users from protected pages (projects, matrix…) to `/signin`. (Mark stretch if needed.)

## In scope
- `pages/login.astro`, `pages/signin.astro`, `pages/register.astro`, `components/AuthForm.vue`, `components/header.astro` (+ new `AuthNav.vue`), auth store integration.

## Out of scope
- Signup flow (#92), backend changes (#52), store creation (#53), tests (#50).

## Acceptance criteria
- [ ] `npm run build` passes.
- [ ] Exactly one login page exists; old paths deleted or redirecting.
- [ ] Login with valid creds sets stores, updates header state, navigates home — with **no alert(), no console.log of tokens**.
- [ ] Login with bad creds shows inline error (not alert).
- [ ] No hardcoded `localhost:8000` in the component.
- [ ] Refresh token is stored (not discarded).
- [ ] Header shows logout when logged in; logout clears state and returns to login.

## Test plan (test-first, implemented in #50)
Component tests: renders form; submit success calls store login + navigates; submit failure shows error message; loading state disables button. See `docs/specs/50/spec.md`.

## Risks
- `/signin` vs `/login` references scattered in templates — grep and update all.
- Header is an Astro component — needs a Vue island for reactivity (Astro can't re-render on store change).
- Backend endpoint for subscription status must land in #52 first or login breaks (coordinate).

## Open questions (your call)
1. Canonical route: `/signin` or `/login`?
2. Do you want to write the `AuthForm.vue` refactor yourself, with AI doing page deletion + header + grunt? (I recommend: you own AuthForm, AI owns the rest.)
3. Route guards in this issue or a separate one?
4. `src/lib/lib.ts` is dead code but issue #44 (GitHub sync) plans to use it — delete now and recreate in #44, or leave it?

## Audit addendum (Ornith 35B frontend audit)
- **Accessibility**: labels don't associate with inputs (no `for`/`id`); add `autocomplete` (`username`, `current-password`) — audit finding 3.2.
- **Token leak**: `AuthForm.vue:54` and `:77` `console.log` the raw access token — must go (finding 4.2).
- **Service worker caches authed pages** (`public/sw.js` caches `/projects`, `/matrix`, `/settings`…) with a cache-first fallback for any GET — logged-in page contents served offline to anyone with device access (finding 4.5). Weekend decision: fix here (network-first for authed routes) or file as separate issue.
- **`index.astro` imports Header but never renders it** — trivial dead import, safe grunt delete (finding 3.4).
- **Error UX**: replace `alert()` with an accessible toast/live-region shared with #92 (finding 3.3) — coordinate one shared `Toast.vue` or store-based toast.
- All nav links already point to `/signin` (no `/login` references found) — deleting `login.astro` is safe; no redirect needed unless you want URL compat.
