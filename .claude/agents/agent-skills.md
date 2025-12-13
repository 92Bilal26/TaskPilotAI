# Autonomous Agent Skills

The autonomous agent has access to these skills to complete Phase 2 implementation independently:

---

## Skill 1: Code Generation

**Purpose**: Generate code from specifications

**When Used**:
- Creating backend models (SQLModel)
- Creating API endpoints (FastAPI routes)
- Creating frontend pages (Next.js)
- Creating components (React)
- Creating tests (pytest, Jest)

**Execution**:
```
Agent: "I will now generate the backend/models.py file with SQLModel definitions"
→ Generate complete, working code
→ Apply code quality checks (mypy, flake8)
→ Commit to phase-2 branch
```

**Examples**:
- Generate `backend/models.py` with Task and User models
- Generate `frontend/components/TaskForm.tsx` with form logic
- Generate `backend/routes/tasks.py` with all 6 endpoints

---

## Skill 2: Test Generation

**Purpose**: Generate tests for Phase 2 components

**When Used**:
- After creating models (unit tests)
- After creating API endpoints (integration tests)
- After creating components (component tests)

**Execution**:
```
Agent: "I will now generate tests for authentication"
→ Create test file with fixtures and test cases
→ Run tests (pytest or Jest)
→ Verify coverage ≥95% (backend) / ≥90% (frontend)
→ Report coverage metrics
```

**Coverage Requirements**:
- Backend: ≥95% code coverage (mypy + flake8 + pytest)
- Frontend: ≥90% code coverage (TypeScript + ESLint + Jest)

**Examples**:
- Generate `backend/tests/test_auth.py` with 8+ test cases
- Generate `backend/tests/test_tasks.py` with 20+ test cases
- Generate `frontend/tests/task-list.test.tsx` with component tests

---

## Skill 3: Documentation

**Purpose**: Generate and update documentation

**When Used**:
- Phase completion
- Architecture changes
- API changes
- Setup instructions

**Execution**:
```
Agent: "I will now update documentation for Phase 3 completion"
→ Update README.md with phase progress
→ Update CLAUDE.md with new patterns
→ Add docstrings to generated code
→ Update architecture diagram
```

**Examples**:
- Add "Phase 2 Setup" section to README.md
- Update backend/CLAUDE.md with FastAPI patterns
- Add docstrings to all Python functions

---

## Skill 4: Git Operations

**Purpose**: Commit changes to version control

**When Used**:
- After phase completion
- After bug fixes
- Before deploying

**Execution**:
```
Agent: "Phase 1 setup complete, committing..."
→ Stage all changes: git add .
→ Create commit with message: "Phase 1: Setup - Backend and frontend initialization"
→ Log commit hash and message
```

**Commit Messages**:
- Format: "Phase X: [Feature] - [Description]"
- Example: "Phase 1: Setup - Backend and frontend project initialization"
- Always includes: `🤖 Generated with Autonomous Agent`

---

## Skill 5: Code Review

**Purpose**: Review code for quality

**When Used**:
- After code generation
- Before commits
- Periodically during development

**Execution**:
```
Agent: "Reviewing Phase 2 code quality..."
→ Run mypy (Python type checking)
→ Run flake8 (Python linting)
→ Run TypeScript compiler (tsc)
→ Run ESLint (JavaScript linting)
→ Report any issues and auto-fix if possible
```

**Checklist**:
- ✅ Type errors: 0
- ✅ Linting errors: 0
- ✅ Test coverage: ≥95% (backend), ≥90% (frontend)
- ✅ No hardcoded secrets
- ✅ User isolation enforced
- ✅ Error handling complete

---

## Skill 6: Deployment

**Purpose**: Deploy code to hosting platforms

**When Used**:
- Phase 6: Integration & Deployment
- Final verification

**Execution**:
```
Agent: "Deploying frontend to Vercel..."
→ Verify build succeeds: npm run build
→ Connect to Vercel (or use CLI)
→ Deploy: vercel --prod
→ Test deployed endpoint
→ Verify: http://[app].vercel.app works
```

**Deployment Targets**:
- Frontend: Vercel
- Backend: Railway, Heroku, or custom server
- Database: Neon PostgreSQL

---

## Skill 7: Debugging

**Purpose**: Fix errors and issues

**When Used**:
- Tests fail
- Type errors occur
- Features don't work
- Deployment issues

**Execution**:
```
Agent: "Debugging test failure in test_auth.py..."
→ Read error message
→ Identify root cause
→ Generate fix
→ Run tests again
→ Verify fix works
→ Document fix in code comment
```

**Process**:
1. Identify error
2. Isolate root cause
3. Generate minimal fix
4. Test fix
5. Verify no regressions
6. Document cause and solution

---

## Skill 8: Refactoring

**Purpose**: Improve code quality without changing functionality

**When Used**:
- After features are working
- Phase 7: Polish & Testing
- Reduce code duplication

**Execution**:
```
Agent: "Refactoring API client for reusability..."
→ Identify repetitive patterns
→ Extract common logic
→ Update tests to match
→ Verify all tests pass
→ Commit refactoring
```

**Targets**:
- Extract helper functions
- Create reusable components
- Reduce duplication
- Improve readability

---

## Skill Usage in Phases

### Phase 1: Setup (T001-T015)
- **Skills**: Code Generation, Git Operations
- **Output**: Project structure, config files
- **Commits**: 2-3 commits per setup area

### Phase 2: Foundational (T016-T034)
- **Skills**: Code Generation, Test Generation, Code Review
- **Output**: Base models, schemas, middleware
- **Commits**: 1 commit (foundational complete)

### Phase 3: Authentication (T035-T079)
- **Skills**: Code Generation, Test Generation, Code Review, Debugging
- **Output**: Auth endpoints, frontend forms, tests
- **Commits**: 1 commit (auth complete)

### Phase 4: CRUD (T080-T144)
- **Skills**: Code Generation, Test Generation, Code Review, Debugging
- **Output**: 6 API endpoints, task components, tests
- **Commits**: 1 commit (CRUD complete)

### Phase 5: Filtering (T145-T167)
- **Skills**: Code Generation, Test Generation, Code Review
- **Output**: Filter endpoints, filter UI, tests
- **Commits**: 1 commit (filtering complete)

### Phase 6: Integration (T168-T205)
- **Skills**: Code Review, Debugging, Deployment, Documentation
- **Output**: Working application, deployment ready
- **Commits**: 1 commit (integration complete)

### Phase 7: Polish (T206-T230)
- **Skills**: Code Review, Refactoring, Documentation, Debugging
- **Output**: Production-ready code, complete docs
- **Commits**: 1 commit (polish complete)

---

## Auto-Option Selection Examples

### Example 1: Framework Selection
```
Claude: "Should we use React or Vue.js for the frontend?"

Agent Decision Logic:
- Rule: "Use specified in spec (highest priority)"
- Spec says: "Next.js 16+ with React"
- Agent selects: ✓ React (matches spec)
- Logs: "Auto-selected React per Phase 2 spec"
```

### Example 2: Testing Approach
```
Claude: "Test-first (TDD) or write tests after code?"

Agent Decision Logic:
- Rule: "Test-First per constitution"
- Constitution says: ≥95% coverage required
- Agent selects: ✓ Test-First (Red-Green-Refactor)
- Logs: "Auto-selected TDD per constitutional requirement"
```

### Example 3: Scope Selection
```
Claude: "Should we implement MVP or full scope?"

Agent Decision Logic:
- Rule: "Full feature scope (complete user story)"
- Reasoning: "Reduces rework"
- Agent selects: ✓ Full scope
- Logs: "Auto-selected full scope for complete functionality"
```

### Example 4: Database Choice
```
Claude: "Use PostgreSQL or MySQL for tasks table?"

Agent Decision Logic:
- Rule: "Persistent PostgreSQL (per spec)"
- Spec says: "Neon Serverless PostgreSQL"
- Agent selects: ✓ PostgreSQL Neon
- Logs: "Auto-selected Neon per Phase 2 spec"
```

---

## Next Step Decision Examples

### After Phase 1 (Setup)
```
Agent: "Phase 1: Setup complete"
↓
Next Step Rule: "Move to Phase 2: Foundational"
↓
Agent Decides: "Proceeding with Phase 2: Foundational Infrastructure"
↓
Action: Start foundational tasks (T016-T034)
```

### After Phase 3 (Authentication)
```
Agent: "Phase 3: Authentication complete"
↓
Next Step Rule: "Start Phase 4: Task CRUD"
↓
Agent Decides: "Proceeding with Phase 4: Task CRUD Operations"
↓
Action: Start CRUD tasks (T080-T144)
```

### After Phase 6 (Integration)
```
Agent: "Phase 6: Integration complete"
↓
Next Step Rule: "Start Phase 7: Polish & Testing"
↓
Agent Decides: "Proceeding with Phase 7: Polish & Testing"
↓
Action: Start polish tasks (T206-T230)
```

---

## Safety Boundaries

The agent respects these safety boundaries:

1. **Data Loss Prevention**
   - Never delete code without backup
   - Always commit before major changes
   - Verify git status before operations

2. **Secret Protection**
   - Scan code for hardcoded secrets
   - Check .env files are in .gitignore
   - Warn on credential detection

3. **Regression Prevention**
   - Run all tests before commit
   - Verify no features broken
   - Compare before/after behavior

4. **Quality Requirements**
   - Enforce type checking (mypy, TypeScript)
   - Enforce linting (flake8, ESLint)
   - Enforce test coverage (≥95%/≥90%)
   - Enforce user isolation (3-level check)

---

## Invocation

The agent is invoked via:

```bash
# Demo mode (safe testing)
python .claude/agents/autonomous_agent.py --demo

# Run from Phase 1
python .claude/agents/autonomous_agent.py --start-phase 1 --auto-commit

# Run with specific config
python .claude/agents/autonomous_agent.py --config .claude/agents/autonomous-agent-config.yaml --mode phase2
```

---

## Monitoring Agent Progress

The agent logs to:
- `/home/bilal/TaskPilotAI/.claude/agents/agent-execution.log` (detailed logs)
- `/home/bilal/TaskPilotAI/.claude/agents/agent-execution.json` (structured data)

View logs:
```bash
tail -f .claude/agents/agent-execution.log
```

---

**Skills System Ready** ✅ The autonomous agent can now execute Phase 2 implementation independently.
