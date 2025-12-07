# TaskPilot Blueprint Implementation Guide

This guide explains how to integrate and use the TaskPilot Blueprint skill within Claude Code and the Claude Agent SDK.

## Overview

The TaskPilot Blueprint is a reusable skill that generates production-ready task management applications. It's designed to be:

- **Portable** - Works across Claude apps, Claude Code, and the API
- **Composable** - Can be combined with other skills
- **Efficient** - Only loads necessary components
- **Powerful** - Includes executable generation scripts

## Architecture

The skill consists of 4 main components:

```
taskpilot-blueprint/
├── README.md                      # Skill overview
├── SUBAGENTS.md                   # Subagent specifications
├── IMPLEMENTATION_GUIDE.md        # This file
├── skill-definition.yaml          # Skill metadata
├── manifest.json                  # Skill manifest
├── scripts/
│   ├── generate-project.sh       # Main generation script
│   ├── validate-output.sh        # Validation script
│   └── setup-git.sh              # Git initialization
└── templates/
    ├── constitution-template.md
    ├── feature-spec-template.md
    ├── api-contract-template.md
    ├── *-template.py
    └── *-template.md
```

## Installation

### Option 1: Clone from GitHub

```bash
cd ~/.claude/skills/
git clone https://github.com/92Bilal26/TaskPilotAI.git taskpilot-blueprint
```

### Option 2: Manual Setup

```bash
mkdir -p ~/.claude/skills/taskpilot-blueprint
cp -r ./.claude/skills/taskpilot-blueprint/* ~/.claude/skills/taskpilot-blueprint/
```

### Option 3: Use in Claude Code (Current Project)

The skill is automatically available when in the TaskPilotAI project:

```bash
cd /path/to/TaskPilotAI
claude-code
# Now run: /blueprint-generate MyApp
```

## Usage Patterns

### Pattern 1: Simple Generation

```bash
/blueprint-generate MyTaskApp
```

This generates a complete project with:
- 5 core features
- 84 tests
- Full specifications
- Interactive UI
- Complete documentation

### Pattern 2: Customized Generation

```bash
/blueprint-generate CompanyTasks \
  --description "Enterprise task manager" \
  --features "priorities,due-dates,tags" \
  --style "dark" \
  --database "sql" \
  --target "~/projects/"
```

### Pattern 3: Programmatic Usage (Claude Agent SDK)

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

const result = query({
  prompt: "Use the taskpilot-blueprint skill to generate MyApp with priorities and due dates",
  options: {
    skills: ['taskpilot-blueprint'],
    agents: {
      'spec-generator': { /* ... */ },
      'code-generator': { /* ... */ },
      'test-generator': { /* ... */ },
      'documentation-generator': { /* ... */ }
    }
  }
});

for await (const message of result) {
  console.log(message);
}
```

## Subagent Integration

The skill works with 4 specialized subagents:

### 1. Spec-Generator Subagent

**Responsibility**: Generate all specification files

```python
def spec_generator(
    app_name: str,
    description: str,
    features: List[str],
    database: str
) -> SpecificationOutput:
    """Generate specification files"""
    # Creates:
    # - constitution.md (8 gates)
    # - overview.md
    # - data-models.md
    # - features/*.md (5 files)
    # - contracts/*.md (5 files)
    # - plan.md (500+ lines)
    # - tasks.md (31 tasks)
```

### 2. Code-Generator Subagent

**Responsibility**: Generate source code

```python
def code_generator(
    app_name: str,
    database: str,
    include_tui: bool,
    python_version: str
) -> CodeOutput:
    """Generate Python source code"""
    # Creates:
    # - src/main.py (242 lines)
    # - src/tui.py (386 lines, optional)
    # - src/commands.py (232 lines)
    # - src/models.py (89 lines)
    # - src/storage.py (38 lines)
    # - src/__init__.py
    # - src/py.typed
```

### 3. Test-Generator Subagent

**Responsibility**: Generate test suite

```python
def test_generator(
    app_name: str,
    features: List[str]
) -> TestOutput:
    """Generate comprehensive test suite"""
    # Creates:
    # - tests/conftest.py (fixtures)
    # - tests/test_add_task.py (18 tests)
    # - tests/test_delete_task.py (13 tests)
    # - tests/test_update_task.py (18 tests)
    # - tests/test_view_tasks.py (22 tests)
    # - tests/test_mark_complete.py (13 tests)
    # Total: 84 tests, 100% pass rate
```

### 4. Documentation-Generator Subagent

**Responsibility**: Generate guides and documentation

```python
def documentation_generator(
    app_name: str,
    include_tui: bool,
    features: List[str]
) -> DocumentationOutput:
    """Generate comprehensive documentation"""
    # Creates:
    # - README.md (400+ lines)
    # - CLAUDE.md (340+ lines)
    # - QUICK_START.md (400+ lines)
    # - TUI_GUIDE.md (400+ lines)
    # - TESTING_GUIDE.md (475+ lines)
    # - PHASE_1_VERIFICATION.md
```

## Execution Flow

```
User Input
    ↓
/blueprint-generate MyApp [options]
    ↓
Parse Arguments & Validate Inputs
    ↓
Initialize Project Structure
    ↓
┌─────────────────────────────┐
│  Spec-Generator Subagent    │  (Parallel Execution)
│  (Creates specifications)    │         +
└─────────────────────────────┘         |
    ↓                                   |
Specifications Ready              ┌─────┴──────────────────┐
    ↓                             ↓                        ↓
    └─────────────────────→ Code-Generator        Test-Generator
                                 ↓                        ↓
                            Source Code              Test Suite
                                 ↓                        ↓
                                 │                        │
                                 └──────────┬─────────────┘
                                           ↓
                              Documentation-Generator
                                           ↓
                                   Documentation Files
                                           ↓
                                  Validate Project
                                           ↓
                                 Initialize Git Repo
                                           ↓
                               Generate Summary Report
                                           ↓
                                  Project Ready!
```

## Quality Validation

Each generated project is validated against:

```python
validation_gates = {
    'test_coverage': 'pytest: 84/84 tests passing',
    'type_safety': 'mypy: 0 errors (strict mode)',
    'code_style': 'flake8: 0 errors (PEP 8)',
    'coverage': 'code coverage: ~97.5%',
    'type_hints': '100% type hint coverage',
    'dependencies': '0 external dependencies',
    'documentation': '3,500+ lines',
    'specifications': '7 files, 6,000+ lines'
}

all_gates_pass = all(validate(gate) for gate in validation_gates)
assert all_gates_pass, "Validation failed"
```

## Template System

The skill includes templates for all component types:

### Specification Templates
- `constitution-template.md` - Project constitution (8 gates)
- `feature-spec-template.md` - Feature specification
- `api-contract-template.md` - API contract definition
- `plan-template.md` - Implementation plan
- `tasks-template.md` - Task breakdown

### Code Templates
- `main.py.template` - CLI entry point
- `tui.py.template` - Interactive UI
- `commands.py.template` - Feature implementations
- `models.py.template` - Data model
- `storage.py.template` - Storage layer

### Test Templates
- `test-template.py` - Test case template
- `conftest.py.template` - Pytest fixtures

### Configuration Templates
- `pyproject.toml.template` - Project configuration
- `pytest.ini.template` - Pytest configuration
- `gitignore.template` - Git ignore rules

### Documentation Templates
- `README.md.template` - Project overview
- `CLAUDE.md.template` - Development guide
- `QUICK_START.md.template` - Quick start
- `TUI_GUIDE.md.template` - UI guide
- `TESTING_GUIDE.md.template` - Testing guide

## Customization

### Adding New Features

To add new optional features:

1. Create feature specification template
2. Add code generation template
3. Add test template
4. Update documentation templates
5. Register in skill-definition.yaml

### Extending Templates

Templates use variable substitution:

```
{{APP_NAME}}          → Application name
{{APP_DESCRIPTION}}   → Application description
{{FEATURE_LIST}}      → Comma-separated features
{{DATABASE}}          → Storage backend choice
{{STYLE}}             → UI style (light/dark/auto)
{{PYTHON_VERSION}}    → Target Python version
{{TIMESTAMP}}         → Generation timestamp
```

### Creating Variants

You can create skill variants for different use cases:

- `taskpilot-blueprint-web` - For Phase 2 (web apps)
- `taskpilot-blueprint-ai` - For Phase 3 (chatbots)
- `taskpilot-blueprint-enterprise` - For multi-user apps

## Error Handling

The skill handles errors gracefully:

```
Generation Error
    ↓
Capture Error Details
    ↓
Log Error Location (Which Subagent)
    ↓
Provide User Feedback
    ↓
Suggest Fixes (if applicable)
    ↓
Allow User to Retry Subagent
```

## Performance Optimization

The skill is optimized for performance:

1. **Parallel Subagent Execution** - Code, Test, and Docs run simultaneously
2. **Lazy Template Loading** - Templates loaded only when needed
3. **Caching** - Reusable components cached
4. **Efficient Validation** - Minimal redundant checks

Typical times:
- Specifications: 2-5 minutes
- Code Generation: 3-5 minutes
- Test Generation: 2-3 minutes
- Documentation: 1-2 minutes
- Validation: 2-3 minutes
- **Total: 10-30 minutes**

## Integration with Existing Projects

To use the skill to extend an existing project:

```
/blueprint-generate ExistingApp --target "~/existing-project/"
```

This will:
1. Preserve existing files
2. Merge specifications
3. Extend code modules
4. Add new tests
5. Update documentation

## Monitoring and Logging

The skill logs generation progress:

```
[Step 1] Validating inputs...
[Step 2] Creating project structure...
[Step 3] Copying templates...
[Step 4] Generating specifications...
[Step 5] Generating code...
[Step 6] Generating tests...
[Step 7] Generating documentation...
[Step 8] Validating project...
[Step 9] Initializing Git...
[Step 10] Preparing summary...
```

## Troubleshooting

### Issue: Subagent timeout

**Solution**: Increase timeout in skill configuration

### Issue: Validation fails

**Solution**: Check generated files for completeness

### Issue: Git initialization fails

**Solution**: Ensure write permissions in target directory

## Future Enhancements

Phase 2+ will add:

- **Web Application Generation** - Full-stack with Next.js + FastAPI
- **Database Schemas** - SQLModel + migrations
- **Kubernetes Deployment** - Docker + Helm charts
- **AI Integration** - Chatbot and agent generation
- **Multi-language** - JavaScript, TypeScript, Go support

## Contributing

To contribute improvements to the skill:

1. Fork the TaskPilotAI repository
2. Create a feature branch
3. Make changes to templates or subagent prompts
4. Test thoroughly
5. Submit a pull request

## License

The TaskPilot Blueprint skill is part of the TaskPilotAI project and follows the same license.

## Support

For questions or issues:

1. Check the skill README.md
2. Review this implementation guide
3. Check subagent specifications in SUBAGENTS.md
4. Open an issue on GitHub

---

**Version**: 1.0.0
**Last Updated**: 2025-12-07
**Status**: Production Ready
