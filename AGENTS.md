# Virtua Tracker - Agent Guidelines

## Build/Lint/Test Commands

### Frontend (Astro + Vue)
- **Development**: `npm run dev`
- **Build**: `npm run build` (includes `astro check`)
- **Preview**: `npm run preview`
- **Mock API**: `npm run api` (json-server on port 3000)

### Backend (Django)
- **Development**: `python manage.py runserver`
- **Migrations**: `python manage.py makemigrations && python manage.py migrate`
- **Create superuser**: `python manage.py createsuperuser`
- **Run tests**: `python manage.py test`
- **Shell**: `python manage.py shell`

### Running Single Tests
- **Django**: `python manage.py test api.tests.TestClass.test_method`
- **Frontend**: No specific test runner configured yet

## Code Style Guidelines

### Vue Components
- Use single-file components with `<template>`, `<script>`, `<style>` structure
- Component names: PascalCase (e.g., `ProjectMatrix.vue`)
- Props: camelCase in script, kebab-case in template
- Events: camelCase (e.g., `@created="handleCreated"`)
- Data properties: camelCase
- Methods: camelCase, descriptive names
- Mixins: Use for shared auth logic (e.g., `authStatus.js`)

### Django Models
- Model names: PascalCase, singular (e.g., `class Issue`)
- Field names: snake_case
- Use `choices` for enums (e.g., `PRIORITY_CHOICES`, `STATUS_CHOICES`)
- Foreign keys: `related_name` for reverse relationships
- String representation: Implement `__str__` method

### API Design
- RESTful endpoints under `/api/`
- JWT authentication with `Authorization: Bearer <token>`
- Use DRF serializers for validation
- Error responses: Standard HTTP status codes

### JavaScript/TypeScript
- ES6+ syntax preferred
- Async/await for API calls
- Local storage for client-side persistence
- Error handling: Try/catch with console.error for debugging

### Python
- Follow PEP 8 style guide
- Use type hints where beneficial
- Import organization: Standard library, third-party, local
- Exception handling: Specific exceptions over bare `except`

### Naming Conventions
- Files: kebab-case for Vue/Astro (e.g., `project-matrix.vue`), snake_case for Python
- Variables: camelCase in JS/Vue, snake_case in Python
- Constants: UPPER_SNAKE_CASE
- Database: snake_case table/column names (Django default)

### Error Handling
- Frontend: User-friendly alerts for API errors
- Backend: Proper HTTP status codes and error messages
- Validation: Client and server-side validation
- Logging: Use console.error for debugging, proper logging in production

### Security
- JWT tokens stored in localStorage (consider httpOnly cookies for production)
- CORS headers configured for cross-origin requests
- Input validation on all API endpoints
- No secrets committed to repository

### File Organization
- Frontend: Feature-based components in `/src/components/`
- Backend: Django apps in `/core/api/`
- Static assets: `/public/` directory
- Configuration: Root-level config files (astro.config.mjs, etc.)

### Git Workflow
- Feature branches from main
- Commit messages: Imperative mood, concise
- Pull requests: Describe changes and testing done
- No direct commits to main branch</content>
<parameter name="filePath">AGENTS.md