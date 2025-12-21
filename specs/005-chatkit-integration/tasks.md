# Implementation Tasks: ChatKit Integration with Agent Builder Workflow

**Feature**: ChatKit Integration
**Branch**: `005-chatkit-integration`
**Created**: December 20, 2025
**Status**: Ready for Implementation
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Task Summary

| Phase | Name | Tasks | Dependencies |
|-------|------|-------|--------------|
| 1 | Setup & Infrastructure | 3 | None |
| 2 | Foundational Backend | 4 | Phase 1 |
| 3 | User Story 1: Session Initiation | 5 | Phase 2 |
| 4 | User Story 2: Message Exchange | 3 | Phase 3 |
| 5 | User Story 3: Backend Sessions | 4 | Phase 2 |
| 6 | User Story 4: Frontend Configuration | 4 | Phase 2 |
| 7 | Integration & Testing | 3 | All user stories |
| 8 | Production Deployment | 3 | Phase 7 |

**Total Tasks**: 29
**Parallel Opportunities**: 3 independent paths (Stories 2, 3, 4 can run in parallel after Phase 2)

---

## Phase 1: Setup & Infrastructure

**Goal**: Initialize project structure and configure dependencies

- [ ] T001 Add ChatKit SDK dependencies to backend/requirements.txt
  - Add: `openai>=1.12.0`, `openai-chatkit>=0.1.0`
  - Update: `backend/requirements.txt`

- [ ] T002 Add ChatKit React package to frontend package.json
  - Add: `@openai/chatkit-react` to dependencies
  - Run: `npm install`
  - Update: `frontend/package.json`

- [ ] T003 Create ChatKit routes structure in backend
  - Create: `backend/routes/chatkit.py` (empty file with router setup)
  - Import router in: `backend/main.py`
  - Add route prefix: `/api/chatkit`

---

## Phase 2: Foundational Backend Setup

**Goal**: Establish session endpoint and core backend infrastructure

**Dependencies**: Complete Phase 1

- [ ] T004 Configure OpenAI SDK initialization in backend
  - File: `backend/main.py`
  - Initialize: `client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))`
  - Validate: Environment variables OPENAI_API_KEY and CHATKIT_WORKFLOW_ID

- [ ] T005 Create ChatKit session endpoint with error handling
  - File: `backend/routes/chatkit.py`
  - Endpoint: `POST /api/chatkit/sessions`
  - Return: `{"status": "success", "data": {"client_secret": "...", "session_id": "..."}}`
  - Errors: Handle 401 (invalid API key), 500 (OpenAI service error), 503 (unavailable)

- [ ] T006 Create test file structure for backend ChatKit tests
  - Create: `backend/tests/test_chatkit.py`
  - Imports: pytest, FastAPI TestClient
  - Setup: fixtures for empty app state

- [ ] T007 Configure CORS for ChatKit endpoints in backend
  - File: `backend/main.py`
  - Add origins: `http://localhost:3000`, `https://task-pilot-ai-ashen.vercel.app`
  - Allow: credentials, methods, headers (standard CORS config)

---

## Phase 3: User Story 1 - User Initiates Chat Session (P1)

**Goal**: Enable users to navigate to ChatKit page and establish session
**Independent Test**: Page loads → Session created → ChatKit initializes
**Acceptance Criteria**:
- ChatKit page loads within 3 seconds
- Session endpoint responds within 2 seconds
- Client secret returned and passed to ChatKit
- User can interact with input field

**Dependencies**: Complete Phase 2

### Tests (Optional - TDD approach)

- [ ] T008 [P] [US1] Write test: ChatKit page renders successfully
  - File: `frontend/components/__tests__/ChatKit.test.tsx`
  - Test: Page loads without errors
  - Verify: Header, input field, loading state visible

- [ ] T009 [P] [US1] Write test: getClientSecret() retrieves valid secret
  - File: `frontend/lib/__tests__/chatkit-config.test.ts`
  - Mock: Fetch to return valid session response
  - Verify: Function returns non-empty string starting with "cs_"

- [ ] T010 [US1] Write test: Backend session endpoint returns valid response
  - File: `backend/tests/test_chatkit.py::test_create_session_success`
  - Mock: OpenAI SDK
  - Verify: Response has status "success", client_secret, session_id

### Implementation

- [ ] T011 [US1] Create ChatKit page component with loading state
  - File: `frontend/app/chatkit/page.tsx`
  - Include: Header, loading spinner, error handling
  - Layout: Responsive container, full height
  - Styling: Match existing TaskPilotAI design

- [ ] T012 [P] [US1] Create ChatKit configuration file with getClientSecret()
  - File: `frontend/lib/chatkit-config.ts`
  - Function: `getClientSecret(existing?: string): Promise<string>`
  - Behavior: Reuse existing, else call backend `/api/chatkit/sessions`
  - Error handling: Console logging, throw on failure

- [ ] T013 [US1] Add ChatKit JS library script tag to layout
  - File: `frontend/app/layout.tsx`
  - Add to `<head>`: `<script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async></script>`

- [ ] T014 [US1] Create ChatKit React component wrapper
  - File: `frontend/components/ChatKitComponent.tsx`
  - Hook: `useChatKit(chatKitConfig)`
  - Render: ChatKit component with config
  - Props: Accept config object

- [ ] T015 [US1] Integrate ChatKit component into page and test session creation
  - File: `frontend/app/chatkit/page.tsx`
  - Import: ChatKitComponent from components
  - Test: Manually verify page loads, session created, ChatKit initializes
  - Browser console: Should show "Got ChatKit session: ses_..."

---

## Phase 4: User Story 2 - User Sends Message to Agent (P1)

**Goal**: Enable message sending and receiving through ChatKit
**Independent Test**: Send message → Agent responds → Response displayed
**Acceptance Criteria**:
- Message appears in chat immediately
- Agent responds within 5 seconds
- Full response visible without truncation
- No errors in console

**Dependencies**: Complete Phase 3 (Session must work first)

**Note**: Message handling is ChatKit's responsibility (not custom implementation)

### Tests (Optional - TDD approach)

- [ ] T016 [P] [US2] Write test: User can type in input field
  - File: `frontend/components/__tests__/ChatKit.test.tsx`
  - Test: Input field accepts text
  - Verify: Input value updates

- [ ] T017 [P] [US2] Write test: Message displays in chat after send
  - File: `frontend/components/__tests__/ChatKit.test.tsx`
  - Test: Mock ChatKit, simulate message send
  - Verify: Message appears in chat history

### Implementation

- [ ] T018 [US2] Verify ChatKit displays messages correctly
  - File: `frontend/components/ChatKitComponent.tsx`
  - Verify: ChatKit component renders messages
  - Test: Manually send message and verify display
  - Timeout: Messages should appear within 5 seconds

- [ ] T019 [US2] Add error handling for message failures
  - File: `frontend/lib/chatkit-config.ts`
  - Error handler: Catch and log message errors
  - User feedback: Display error message in chat or toast

- [ ] T020 [US2] Test message handling with real agent
  - Manual test: Send test message "Hello"
  - Verify: Agent responds
  - Check: Response fully visible, no truncation

---

## Phase 5: User Story 3 - Backend Creates Secure Sessions (P1)

**Goal**: Implement secure session creation using OpenAI SDK
**Independent Test**: POST /api/chatkit/sessions → returns valid session
**Acceptance Criteria**:
- Session created using OpenAI SDK
- Client secret and session ID returned
- Workflow ID associated but not exposed
- Concurrent requests handled

**Dependencies**: Complete Phase 2

### Tests (Optional - TDD approach)

- [ ] T021 [P] [US3] Write test: Session endpoint returns 200 with data
  - File: `backend/tests/test_chatkit.py::test_create_session_success`
  - Test: POST /api/chatkit/sessions
  - Verify: status_code 200, response has client_secret and session_id

- [ ] T022 [P] [US3] Write test: Invalid API key returns 401
  - File: `backend/tests/test_chatkit.py::test_invalid_api_key`
  - Test: Mock OpenAI API to return auth error
  - Verify: status_code 401, error message returned

- [ ] T023 [P] [US3] Write test: Concurrent requests handled correctly
  - File: `backend/tests/test_chatkit.py::test_concurrent_sessions`
  - Test: 5 simultaneous requests
  - Verify: All return unique session IDs

### Implementation

- [ ] T024 [US3] Implement OpenAI SDK call in session endpoint
  - File: `backend/routes/chatkit.py::create_chatkit_session`
  - Call: `client.chatkit.sessions.create(workflow={"id": WORKFLOW_ID})`
  - Extract: client_secret and session_id from response

- [ ] T025 [US3] Add validation for OpenAI configuration
  - File: `backend/routes/chatkit.py`
  - Validate: OPENAI_API_KEY present and valid
  - Validate: CHATKIT_WORKFLOW_ID present and matches expected value
  - Error: Return 500 with descriptive message if validation fails

- [ ] T026 [US3] Add logging for session creation (audit trail)
  - File: `backend/routes/chatkit.py`
  - Log: session_id, user_id (if available), created_at timestamp
  - Security: Do NOT log client_secret or API key

- [ ] T027 [US3] Test session endpoint directly
  - Command: `curl -X POST http://localhost:8000/api/chatkit/sessions`
  - Verify: Returns 200 with client_secret and session_id
  - Test with invalid key: Verify error handling

---

## Phase 6: User Story 4 - Frontend Configuration Enables ChatKit (P1)

**Goal**: Configure frontend to retrieve and use session secrets
**Independent Test**: Config loads → getClientSecret() calls backend → ChatKit initializes
**Acceptance Criteria**:
- Config object properly structured
- getClientSecret() function registered
- Backend endpoint called correctly
- ChatKit initializes with secret

**Dependencies**: Complete Phase 2 and Phase 3

### Tests (Optional - TDD approach)

- [ ] T028 [P] [US4] Write test: ChatKit config has required properties
  - File: `frontend/lib/__tests__/chatkit-config.test.ts`
  - Test: Config object structure
  - Verify: api.getClientSecret exists and is function

- [ ] T029 [P] [US4] Write test: getClientSecret() calls correct endpoint
  - File: `frontend/lib/__tests__/chatkit-config.test.ts`
  - Mock: fetch
  - Verify: Called with POST /api/chatkit/sessions

- [ ] T030 [P] [US4] Write test: ChatKit initializes with config
  - File: `frontend/components/__tests__/ChatKit.test.tsx`
  - Test: useChatKit hook receives config
  - Verify: Hook initializes without errors

### Implementation

- [ ] T031 [US4] Finalize chatkit-config.ts with all options
  - File: `frontend/lib/chatkit-config.ts`
  - Config: api.getClientSecret, theme (optional), callbacks
  - Comments: Document each config option
  - Export: Default export of chatKitConfig

- [ ] T032 [US4] Add environment variable support to config
  - File: `frontend/lib/chatkit-config.ts`
  - Use: process.env.NEXT_PUBLIC_API_URL
  - Fallback: http://localhost:8000 for development

- [ ] T033 [US4] Add retry logic to getClientSecret()
  - File: `frontend/lib/chatkit-config.ts`
  - Retry: Up to 3 times on network failure
  - Backoff: Exponential (1s, 2s, 4s)
  - Final error: Show user-friendly message

- [ ] T034 [US4] Test frontend configuration with backend
  - Manual test: Load http://localhost:3000/chatkit
  - Browser console: Verify "Got ChatKit session" message
  - Verify: getClientSecret() called and returned valid secret

---

## Phase 7: Integration & Testing

**Goal**: Verify complete flow and all components work together
**Test Coverage**: End-to-end flow, error scenarios, performance

**Dependencies**: Complete all user story phases

- [ ] T035 [P] Write end-to-end test: Full user flow
  - File: `frontend/components/__tests__/ChatKit.e2e.test.tsx`
  - Scenario: Page load → Session creation → Message send → Response received
  - Verify: All steps complete without errors
  - Timing: Page load <3s, session <2s, response <5s

- [ ] T036 [P] Write integration test: Frontend-Backend communication
  - File: `tests/integration/test_chatkit_flow.py`
  - Test: Frontend can communicate with backend ChatKit endpoint
  - Verify: Session endpoint works with real frontend requests
  - CORS: No CORS errors

- [ ] T037 Test error scenarios and edge cases
  - Scenarios:
    - Backend unavailable → User sees error message with retry
    - Invalid API key → Clear error message
    - Network timeout → Retry logic engages
    - Concurrent requests → All handled correctly
  - File: `backend/tests/test_chatkit.py`, `frontend/components/__tests__/`

---

## Phase 8: Production Deployment

**Goal**: Deploy ChatKit to production with domain registration
**Dependencies**: Complete Phase 7 and all functionality verified

- [ ] T038 Register production domain with OpenAI
  - Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
  - Domain: https://task-pilot-ai-ashen.vercel.app
  - Save: Domain key generated by OpenAI

- [ ] T039 Configure production environment variables in Vercel
  - Vercel Dashboard → Settings → Environment Variables → Production
  - Set: NEXT_PUBLIC_API_URL (production backend URL)
  - Set: NEXT_PUBLIC_CHATKIT_DOMAIN_KEY (from OpenAI)
  - Redeploy: Automatic on variable changes

- [ ] T040 Update backend CORS and deploy to production
  - File: `backend/main.py`
  - Add: https://task-pilot-ai-ashen.vercel.app to allowed_origins
  - Deploy: Push to production (Railway, Render, etc.)
  - Verify: Backend accessible from production frontend

---

## Implementation Strategy

### Phase Execution Order

```
Phase 1 (Setup)
    ↓
Phase 2 (Backend Foundation)
    ├─→ Phase 3 (US1: Sessions)
    ├─→ Phase 4 (US2: Messages) [Parallel, depends on Phase 3]
    ├─→ Phase 5 (US3: Backend Sessions) [Parallel, depends on Phase 2]
    └─→ Phase 6 (US4: Frontend Config) [Parallel, depends on Phase 2]
    ↓
Phase 7 (Integration Testing)
    ↓
Phase 8 (Production Deployment)
```

### Parallel Opportunities

**After Phase 2 completes, these can run in parallel**:
- Phase 3 & Phase 5: Both implement session functionality (frontend & backend can develop independently)
- Phase 4 & Phase 6: Message handling & configuration (independent from each other)

**Recommended parallelization**:
- Developer 1: Phase 3 (Frontend session) + Phase 4 (Messages)
- Developer 2: Phase 5 (Backend sessions) + Phase 6 (Frontend config)
- After parallel work merges → Phase 7 (Integration testing)

### MVP Scope (Minimum for Production)

**If you want fastest deployment to production**:
1. ✅ Phase 1: Setup (required)
2. ✅ Phase 2: Backend foundation (required)
3. ✅ Phase 3: Session initiation (required - core functionality)
4. ⚠️ Phase 4: Messages (highly recommended - provides user value)
5. ✅ Phase 5: Backend sessions (already included in Phase 2)
6. ✅ Phase 6: Frontend config (already included in Phase 3)
7. ⚠️ Phase 7: Integration testing (recommended before production)
8. ✅ Phase 8: Production deployment (required to go live)

**MVP Time Estimate**: 2-4 hours for one developer

### Testing Approach

**Option A: Test-First (TDD)**
- Write tests first (T008-T010, T021-T023, T028-T030)
- Implement code to pass tests
- Best for: Complex logic, confidence in correctness

**Option B: Test-After**
- Implement code (T011-T034)
- Write tests after (T008-T010, T021-T023, T028-T030)
- Best for: Rapid prototyping, learning

**Recommended**: Test-After (pragmatic approach given timeline)

---

## Task Dependencies Diagram

```
T001, T002, T003 (Phase 1: Setup)
        ↓
T004, T005, T006, T007 (Phase 2: Backend Foundation)
        ├─→ T008, T009, T011, T012, T013, T014, T015 (Phase 3: US1)
        ├─→ T021, T022, T023, T024, T025, T026, T027 (Phase 5: US3)
        ├─→ T028, T029, T030, T031, T032, T033, T034 (Phase 6: US4)
        └─→ T016, T017, T018, T019, T020 (Phase 4: US2)
        ↓
T035, T036, T037 (Phase 7: Integration Testing)
        ↓
T038, T039, T040 (Phase 8: Production)
```

---

## Quality Checklist

Before marking each phase complete:

### Phase Completion Criteria

**Phase 1**:
- [ ] Dependencies installed (`pip list`, `npm list`)
- [ ] No import errors

**Phase 2**:
- [ ] Backend starts: `uvicorn main:app --reload`
- [ ] Endpoint registered: Shows in OpenAPI docs
- [ ] No type errors: `mypy backend/`

**Phase 3**:
- [ ] Page loads: http://localhost:3000/chatkit
- [ ] Browser console: "Got ChatKit session"
- [ ] Input field interactive

**Phase 4**:
- [ ] Message sends: User can type and send
- [ ] Response displays: Agent responds within 5s
- [ ] No truncation: Full message visible

**Phase 5**:
- [ ] Endpoint works: `curl -X POST http://localhost:8000/api/chatkit/sessions`
- [ ] Returns valid response: client_secret and session_id
- [ ] Error handling: Test with invalid API key

**Phase 6**:
- [ ] Config loads: No errors
- [ ] Endpoint called: Network tab shows POST to /api/chatkit/sessions
- [ ] ChatKit initializes: Component renders

**Phase 7**:
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Coverage: ≥95% backend, ≥90% frontend
- [ ] No console errors: Browser DevTools clean

**Phase 8**:
- [ ] Domain registered: OpenAI allowlist shows domain
- [ ] Environment vars set: Vercel Dashboard shows values
- [ ] Production URL works: https://task-pilot-ai-ashen.vercel.app/chatkit loads

---

## File Reference

### Backend Files
- `backend/main.py` - OpenAI SDK init, CORS config, router registration
- `backend/routes/chatkit.py` - Session endpoint, error handling, logging
- `backend/requirements.txt` - Dependencies

### Frontend Files
- `frontend/app/chatkit/page.tsx` - ChatKit page component
- `frontend/app/layout.tsx` - ChatKit JS script tag
- `frontend/lib/chatkit-config.ts` - Configuration and getClientSecret
- `frontend/components/ChatKitComponent.tsx` - React wrapper
- `frontend/package.json` - Dependencies

### Test Files
- `backend/tests/test_chatkit.py` - Backend tests
- `frontend/components/__tests__/ChatKit.test.tsx` - Frontend component tests
- `frontend/lib/__tests__/chatkit-config.test.ts` - Config tests

### Configuration Files
- `backend/.env` - OPENAI_API_KEY, CHATKIT_WORKFLOW_ID
- `frontend/.env.local` - NEXT_PUBLIC_API_URL (local)
- `frontend/.env.production.local` - NEXT_PUBLIC_API_URL, NEXT_PUBLIC_CHATKIT_DOMAIN_KEY (production)

---

**Last Updated**: December 20, 2025
**Status**: Ready for Implementation
**Created by**: /sp.tasks workflow
**Next Step**: Begin with Phase 1 tasks
