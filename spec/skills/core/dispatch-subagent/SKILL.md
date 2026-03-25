---
name: dispatch-subagent
description: |
  Dispatch independent tasks to subagents for parallel execution. Use when:
  (1) Plan contains multiple independent tasks
  (2) Tasks have no dependencies on each other
  (3) Need to speed up execution through parallelization
  (4) Each task is self-contained (2-5 minutes of work)
---

# Dispatch Subagent

Execute independent tasks in parallel using subagents for faster completion.

## Input

```yaml
tasks: list           # List of independent tasks
max_parallel: number  # Max concurrent subagents (default: 3)
review_mode: string   # "none" | "spec" | "full" (default: "spec")
```

## Output

```yaml
results: list         # Results from each subagent
all_passed: boolean   # Whether all tasks succeeded
failed_tasks: list    # List of failed task IDs
```

## Checklist

- [ ] Verify tasks are independent (no dependencies)
- [ ] Split plan into dispatchable units
- [ ] Dispatch subagents with clear context
- [ ] Collect and review results
- [ ] Handle failures appropriately

## When to Use

**Good candidates for subagent dispatch:**
- Multiple test files to write
- Independent API endpoints to implement
- Separate UI components to build
- Multiple documentation files to update

**NOT suitable for subagent dispatch:**
- Sequential tasks with dependencies
- Tasks that modify shared state
- Tasks requiring human decisions mid-way

## Execution

### 1. Analyze Task Independence

```
For each task pair (A, B):
  - Does A's output affect B's input? → Dependent
  - Do A and B modify the same files? → Dependent
  - Can A and B run in any order? → Independent
```

### 2. Prepare Subagent Context

Each subagent receives:
```markdown
## Task
{task_description}

## Scope
Files: {file_list}
Tests: {test_expectations}

## Constraints
- Complete THIS task only
- Do NOT modify files outside scope
- Run tests before reporting done

## Success Criteria
{acceptance_criteria}
```

### 3. Dispatch Pattern

```
┌─────────────┐
│   Main      │
│   Agent     │
└──────┬──────┘
       │ dispatch
       ▼
┌──────┴──────┬──────────────┐
│             │              │
▼             ▼              ▼
┌─────┐   ┌─────┐       ┌─────┐
│Sub 1│   │Sub 2│  ...  │Sub N│
└──┬──┘   └──┬──┘       └──┬──┘
   │         │              │
   ▼         ▼              ▼
┌──────┐ ┌──────┐       ┌──────┐
│Result│ │Result│  ...  │Result│
└──┬───┘ └──┬───┘       └──┬───┘
   │         │              │
   └─────────┴──────────────┘
             │ collect
             ▼
      ┌─────────────┐
      │   Review    │
      │   Results   │
      └─────────────┘
```

### 4. Two-Stage Review

**Stage 1: Spec Compliance**
- Did subagent complete the assigned task?
- Are all acceptance criteria met?
- Any scope violations?

**Stage 2: Code Quality** (if review_mode = "full")
- Code follows project standards?
- Tests are meaningful?
- No obvious bugs?

### 5. Handle Failures

```
IF subagent fails:
  1. Log failure reason
  2. Check if other subagents affected
  3. Options:
     a. Retry failed task only
     b. Rollback all changes
     c. Continue with successful tasks
```

## Subagent Template

```markdown
# Subagent Task: {task_id}

You are a subagent with a SINGLE focused task.

## Your Task
{task_description}

## Files You May Modify
{allowed_files}

## Files You May Read
{readable_files}

## DO NOT
- Modify files outside your scope
- Make architectural decisions
- Skip tests
- Ask questions (work with given info)

## When Done
Report:
1. Files modified
2. Tests added/modified
3. Test results
4. Any concerns
```

## Constraints

- Maximum 5 parallel subagents
- Each task must be completable in <10 minutes
- Subagents cannot spawn other subagents
- All results must be reviewed before merge

## Isolation Policy (Shared-Nothing Architecture)

> **Critical**: This policy prevents state conflicts and ensures deterministic execution.

### Golden Rules

| Rule | Description |
|------|-------------|
| **No Global State Writes** | Subagents **MUST NOT** modify `.anrs/state.json` |
| **Exclusive File Scope** | Each subagent owns a disjoint set of files |
| **Orchestrator Merges** | Only Main Agent updates global state after all subagents complete |

### Isolation Boundaries

```
┌─────────────────────────────────────────────────┐
│                 Main Agent                       │
│  ┌─────────────────────────────────────────┐    │
│  │         .anrs/state.json                │    │
│  │         (ONLY Main Agent writes)        │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────┬───────────────────────────┘
                      │ dispatch (read-only snapshot)
         ┌────────────┼────────────┐
         ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │Subagent │  │Subagent │  │Subagent │
    │   A     │  │   B     │  │   C     │
    │         │  │         │  │         │
    │ scope:  │  │ scope:  │  │ scope:  │
    │ src/a/* │  │ src/b/* │  │ src/c/* │
    └────┬────┘  └────┬────┘  └────┬────┘
         │            │            │
         ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ Result  │  │ Result  │  │ Result  │
    │ + Diff  │  │ + Diff  │  │ + Diff  │
    └────┬────┘  └────┬────┘  └────┬────┘
         │            │            │
         └────────────┼────────────┘
                      ▼
              ┌───────────────┐
              │  Main Agent   │
              │  Merge +      │
              │  State Update │
              └───────────────┘
```

### What Subagents Receive

```yaml
# Read-only snapshot (immutable during execution)
state_snapshot:
  current_task: "task-001"
  subtask_id: "task-001-sub-a"
  
# Exclusive write scope
file_scope:
  writable: ["src/module_a/**", "tests/test_module_a.py"]
  readable: ["src/shared/**", "docs/**"]  # read-only
```

### What Subagents Return

```yaml
result:
  status: "success" | "failure"
  files_modified: ["src/module_a/handler.py"]
  files_created: ["tests/test_handler.py"]
  test_results:
    passed: 5
    failed: 0
  errors: []  # Empty if success
```

### Conflict Prevention

1. **Pre-dispatch Validation**
   - Orchestrator verifies file scopes are disjoint
   - If overlap detected → fall back to sequential execution

2. **Post-completion Merge**
   - Orchestrator collects all results
   - Applies changes in deterministic order (by subtask_id)
   - Updates `state.json` once, atomically

3. **Failure Handling**
   - If any subagent fails → Orchestrator decides:
     - Retry failed task only (no global state corruption)
     - Rollback successful tasks (all or nothing)
     - Accept partial (mark failed tasks for retry)

## Integration with ANRS

```
1. READ state.json
2. LOAD plan from .anrs/plans/active/
3. ANALYZE task independence
4. IF independent tasks exist:
   → dispatch-subagent
   → collect results
   → review (spec → quality)
5. ELSE:
   → execute-plan (sequential)
6. RUN harness on combined changes
7. atomic-commit
```

## Related

- `spec/skills/core/execute-plan/` — Sequential execution
- `spec/skills/core/write-plan/` — Create dispatchable plans
- `spec/orchestrator/ORCHESTRATOR.md` — Execution protocol

## Advanced: Physical Isolation with Git Worktree

> **Note**: This is an optional advanced implementation for environments requiring 
> stronger isolation guarantees than Prompt-level constraints.

### When to Use

- High-risk concurrent modifications
- Untrusted or experimental subagent implementations
- Compliance requirements for audit trails

### Implementation Pattern

```bash
# Orchestrator creates isolated worktrees for each subagent
git worktree add ../worktree-sub-a -b task-001-sub-a
git worktree add ../worktree-sub-b -b task-001-sub-b

# Each subagent works in its own worktree (physical isolation)
Subagent-A → ../worktree-sub-a/
Subagent-B → ../worktree-sub-b/

# After completion, Orchestrator merges results
git checkout main
git merge task-001-sub-a --no-ff
git merge task-001-sub-b --no-ff

# Cleanup
git worktree remove ../worktree-sub-a
git worktree remove ../worktree-sub-b
```

### Benefits

| Aspect | Prompt Isolation | Git Worktree |
|--------|------------------|---------------|
| Enforcement | Soft (AI honor system) | Hard (OS-level) |
| Complexity | Low | Medium |
| Conflict Detection | At merge time | Git handles automatically |
| Audit Trail | Requires logging | Built into Git history |

### Trade-offs

- Requires Orchestrator to have Git CLI access
- Adds latency for worktree creation/cleanup
- More complex error handling (merge conflicts)

For most use cases, the default **Shared-Nothing Prompt Isolation** is sufficient.
