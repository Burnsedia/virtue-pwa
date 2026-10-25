# Spec: Refactor Global Auth Stores to Nano Stores — Issue #53

- **Status:** Draft (AI) — awaiting your edit
- **Owner:** You (store design + core) + AI (component migration grunt)
- **Branch:** `feat/53-nano-stores` (created)
- **Blocks:** #49 (login refactor), #92 (signup refactor), #50 (vitest)
- **Priority:** P1

## Background
Auth state lives in raw `localStorage` with a Vue2-style mixin. Nothing is reactive; every component reads `localStorage.getItem('token')` directly. Goal: proper nano stores as the single source of truth, with persistence.

## Current behavior (grounded facts)
- `frontend/src/mixins/authStatus.js`: Vue2 options mixin, reads `localStorage['userStatus']` per computed access. No reactivity across components.
- **No nano stores installed** (`frontend/package.json` has no `nanostores` / `@nanostores/vue` / `@nanostores/persistent`).
- Mixin consumers (7): `OrganizationList.vue`, `KanbanBoard.vue`, `CreateProject.vue`, `ProjectList.vue`, `CreateOrganizationModal.vue`, `PricingPage.vue`, `ProjectMatrix.vue`.
- Direct `localStorage.getItem('token')` in 13+ components: `AuthForm`, `ChangeEmail`, `BillingPortal`, `PomodoroTimer`, `addTask`, `DeleteAccount`, `EditIssueModal`, `ProjectReport`, `CreateIssueModal`, `ChangePassword`, `OrganizationList`, `CreateOrganizationModal`, `ProjectList`, `PricingPage`, `ProjectMatrix`, `KanbanBoard`.
- `AuthForm.vue` writes: `token` (access only — refresh token **discarded**), `userStatus` JSON `{isLoggedIn, isPremium, userId}`.
- `DeleteAccount.vue` removes only `token` (leaves `userStatus` stale).
- Vue version: 3.5 (mixins "work" but are legacy style).

## Proposed store design (edit freely)
File: `frontend/src/lib/stores/authStore.ts` (or `.js` — your call)

- `$token` — atom<string | null>, persisted (`@nanostores/persistent`, key `auth:token`). Also store refresh token: `$refreshToken`.
- `$user` — atom<{id, username, email} | null>, persisted.
- `$isPremium` — atom<boolean>, persisted.
- `isLoggedIn` — computed/derived store: `computed([$token], t => !!t)`.
- Actions: `login(access, refresh, user, isPremium)`, `logout()` (clear all atoms), `getAuthHeaders()` (returns `{Authorization: Bearer ...}` or empty).
- SSR safety: guards via `typeof window` (Astro islands + `client:load` make this easy).

## Migration scope (AI grunt after you design)
1. Add deps: `nanostores`, `@nanostores/vue`, `@nanostores/persistent`.
2. Replace all 13+ `localStorage.getItem('token')` call sites with `$token.get()` / `getAuthHeaders()`.
3. Replace the 7 mixin usages with `useStore($isPremium)` / `$user` from `@nanostores/vue`.
4. Delete `mixins/authStatus.js` once zero consumers remain.
5. `DeleteAccount.vue`: use `logout()` so everything clears.

## In scope
- `frontend/src/lib/stores/` (new), package.json deps, all components listed above, `mixins/authStatus.js` (deletion).

## Out of scope
- Login/signup page behavior changes (#49/#92), header UI changes (do as part of #49), backend.

## Acceptance criteria
- [ ] `npm run build` passes (astro check included).
- [ ] No component reads `localStorage` for auth state directly (grep: only store internals + persistence lib may touch it).
- [ ] `mixins/authStatus.js` deleted; zero imports remain.
- [ ] Logout clears token, refresh token, user, premium flags atomically.
- [ ] SSR build doesn't crash on store import.
- [ ] Existing frontend tests still green (`npm run test:run`).

## Test plan (test-first, implemented in #50)
Store unit tests: login sets atoms + persists, logout clears, `isLoggedIn` derives correctly, `getAuthHeaders` output. See `docs/specs/50/spec.md`.

## Risks
- `@nanostores/persistent` + SSR: ensure persistence only activates on client.
- Large mechanical migration across 13+ files — AI does it, you review the diff carefully.
- Token refresh not handled anywhere yet — the store should hold `$refreshToken` now so #49 can use it.

## Open questions (your call)
1. TypeScript (`authStore.ts`) or JavaScript (`authStore.js`)? Repo mixes both.
2. Persist keys: keep `token`/`userStatus` key names for backward compat, or new `auth:*` namespace?
3. Should `logout()` also call the backend logout endpoint, or purely client-side?
4. Do you want a `$isLoggedIn` atom too, or derived-only?

## Audit addendum (Ornith 35B frontend audit)
- **Two viable designs** — pick one:
  - *(my draft)* separate atoms (`$token`, `$refreshToken`, `$user`, `$isPremium`) + computed `isLoggedIn`, persisted via `@nanostores/persistent`.
  - *(audit proposal)* single `reactiveStore` object `{token, isLoggedIn, isPremium, userId}` + actions module (`login`, `logout`, `register`) — simpler API, one `.set()` per event. Recommend this if you want the migration to be maximally mechanical.
- **Pair the store with a central `api` helper** (`src/lib/api.js`): `api.json('/path', {method, body})` that reads the token from the store and sets `Authorization` — kills 15 copy-pasted `localStorage.getItem('token')` sites AND the 20+ hardcoded `localhost:8000` URLs in one move (audit findings 4.4, 5.3). Strongly recommended; supersedes the "just swap the token read" migration.
- `userId` is stored today but never consumed anywhere — keep it in the store anyway (future profile/settings flows) or drop it, your call.
- `src/lib/lib.ts` is **dead code** (never imported) but issue #44 plans to use it for GitHub sync — don't delete without deciding (see #49 open questions).
- Frontend test `setup.ts` mocks `localStorage.getItem` to return `undefined` — #50 tests need an in-memory mock (see `docs/specs/50/spec.md`).
- 21 Vue files all use Options API; the migration can convert consumers to `<script setup>` + `useStore()` file-by-file — no need to convert untouched components.
