# Issue Triage and Action Plan

## Overview
Based on a codebase audit and review of the 16 open GitHub issues, the current state is characterized by significant "AI slop" (duplicate pages, empty files) and a fragmented authentication implementation.

## 1. Verified & Completed (Proposed for Closure)
The following issues are already implemented in the codebase and should be closed after a brief manual verification:
- **#31: create signup** (Verified: `SignupForm.vue`, `signup.astro` exist)
- **#32: Create Login/Logout Page** (Verified: `login.astro`, `signin.astro` exist)
- **#42: create projects** (Verified: `Project` model, `CreateProject.vue`, `ProjectList.vue` exist)
- **#43: Time Login** (Verified: `TimeLog` model, `TimeLogViewSet` exist; Pomodoro UI exists)
- **#45: Issue Create Model** (Verified: `Issue` model exists)
- **#47: Eisenhower Matrix Project Board** (Verified: `matrix.astro`, `ProjectMatrix.vue` exist)

## 2. Authentication Epic Consolidation
The recent auth-related issues (#49-#56) are overlapping. **#54 (Refactor the SignUp Page)** serves as the parent Epic.

### Epic: #54 Refactor Authentication
**Priority: P0/P1**
**Status: Active**

| Issue | Role | Priority | Notes |
|---|---|---|---|
| **#52** | Base Task | P0 | Refactor Djoser on Django API. Foundation for all auth work. |
| **#51 + #56** | Base Task | P0 | **Merge/Consolidate**: Write backend tests for account/user creation. |
| **#53** | Base Task | P1 | Refactor global auth stores to use **Nano Stores**. |
| **#49** | Refactor Task | P1 | Refactor Login page; remove AI slop/duplication; clean up `signin.astro` vs `login.astro`. |
| **#50** | Test Task | P1 | Write Vitest tests for the new Login logic. |
| **#54 (Remaining)**| Test Task | P1 | E2E tests as per the checklist in #54. |

## 3. Product Backlog & Rescoping
| Issue | Action | Priority | Notes |
|---|---|---|---|
| **#44: Sync GitHub Issues** | Rescope | P2 | Implement two-way sync (currently only reads via `lib.ts`). |
| **#46: Prompt User...** | Keep | P2 | Product feature: issue breakdown wizard. |
| **#48: AI agents...** | Clarify | P3 | Label as `needs-info`. Check if `ProjectReport` satisfies this. |

## 4. Proposed Execution Sequence

1. **GitHub Hygiene**: 
   - Close #31, #32, #42, #43, #45, #47.
   - Label #54 as `epic`.
   - Merge #51 and #56 into one issue.
   - Label others with `tech-debt`, `feature`, or `needs-info`.
2. **Backend Foundation**: Complete **#52** (Djoser) $\rightarrow$ **Merged #51/#56** (Backend tests).
3. **Frontend Foundation**: Complete **#53** (Nano stores).
4. **Refactor & Cleanup**: Complete **#49** (Login refactor + deduplication) $\rightarrow$ **#50** (Vitest).
5. **Finalize Epic**: Complete remaining checklist in **#54** (Signup refactor + E2E).
6. **Backlog**: Address #44, #46, #48 as resources allow.
